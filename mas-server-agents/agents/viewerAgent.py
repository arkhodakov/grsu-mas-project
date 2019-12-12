import json
import types
import osbrain
import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from osbrain import Agent
from lxml.html import fromstring
from urllib.parse import urlparse
from multiprocessing import Pool

# =====> Tools <====== #
from explorer import Explorer

# =====> Models <===== #
# Импорт всех моделей из .py скрипта models.data #
from models.data import *


class ViewerAgent(Agent):
    """
    Агент для исследования и сбора информации о веб-сайтах и вакансиях на этих веб-сайтах.
    
    Получает список веб-адресов (URL адресов) и исследует каждый из них.
    Работа с отдельными веб-сайтами проводится по заранее подготовленным моделям, которые содержат информацию о том,
    как и где на веб-странице искать информацию о вакансиях и что из неё можно достать.
    
    Аттрибуты:
    -------
    headers : dict
        словарь хедеров для сессии модуля requests  
    
    models : array<Model>
        массив моделей для вытягивания информации из веб-страниц
    
    countOfProcesses : int
        количество процессов, создаваемых для работы Explorer'а  
    """

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referer': "https://www.google.by/"
    }

    models = [
        TutBy(),
        Jooble(),
        Belmeta()
    ]
    
    countOfProcesses = 5

    def __contains__(self, x, function):
        for x in self.models:
            if function(x):
                return x
        return None

    def on_init(self):
        self.explorer = Explorer()

    def getUrlPageTitle(self, session: requests.Session, url: str) -> str:
        """
        Делает запрос по URL адресу и возвращает название страницы.
        
        Возвращаемое значение:
        -------
        str
            название страницы
        """
        
        content = session.get(url).content
        return fromstring(content).findtext('.//title')

    def getDefaultSession(self) -> requests.Session:
        """
        Создаёт объект сессии для requests запросов.
        Это необходимо для того, чтобы в том случае, когда сайт ограничивает доступ к себе из-за большого количества наших запросов,
        мы могли переподключиться к нему.
        
        Количество переподключений и время между ними устанавливается параметрами 'connect' и 'bacoff_factor' при создании объекта 'Retry'
        
        Возвращаемое значение:
        -------
        requests.Session
            объект сессии модуля requests
        """
        
        retry = Retry(connect=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers = self.headers
        
        return session

    def exploreUrlAddress(self, url: str) -> dict():
        """
        Исследует один URL адрес: получает его имя, доменное имя, название сайта, его полную ссылку (приходит в параметрах) и вакансии.
        Вакансии достаются в отдельном классе Explorer.
        
        Возвращаемое значение:
        -------
        dict
            словарь с данными о URL адресе
        
        """
        
        self.log_info(" - Processing: %s " % url[:30])
        
        session = self.getDefaultSession()
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))

        info = {
            "name": None,
            "domain": domain,
            "title": self.getUrlPageTitle(session, url),
            "url": url,
            "vacancies": []
        }

        model = self.__contains__(domain, lambda x: x.domain in domain)
        if model is not None:
            if model.blocked == True:
                self.log_info(" ! Model '%s' has been blocked" % model.name)
                return info
            info['name'] = model.name
            content = self.explorer.getContentFromURL(session, url, model)
            info['vacancies'].extend(content)
            self.log_info(" > Content: %s vacancies" % len(content))

        return info

    def handler(self, message: str) -> str:
        """
        Метод для работы с входящими запросами. Вызывается автоматически, когда приходит новый запрос.
        Запускает несколько потоков (по умолчанию - 5) на весь массив URL адресов для более быстрого процесса сбора информации.
        
        Возвращаемое значение:
        ------
        str
            строка (JSON) со всеми url адресами и информацией о них
        """
        
        pool = Pool(countOfProcesses)
        urls = json.loads(message)

        response = pool.map(self.exploreUrlAddress, urls)
        return json.dumps(response)
