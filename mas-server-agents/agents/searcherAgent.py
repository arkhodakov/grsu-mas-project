import osbrain
import json
import googlesearch
from osbrain import Agent

class SearcherAgent(Agent):
    """
    Агент поиска ссылок по запросу в Google. Получает от Google список источников с предполагаемыми вакансиями
    и передаёт этот список Viewer агенту.
    
    Аттрибуты:
    --------
    __viewer__ : str
        константный адрес агента Viewer в osBrain сети (алиас)
    """
    
    __viewer__ = "viewer"

    def sendUrlsToViewer(self, urls: []) -> []:
        """
        Передаёт массив ссылок агенту Viewer.
        
        Возвращаемое значение:
        -------
        array
            информация о веб-страницах и вакансиях, которые удалось на них найти
        """
        
        self.send(self.__viewer__, json.dumps(urls))
        response = self.recv(self.__viewer__)
        return response

    def searchInGoogle(self, message: dict, maxCountOfLinks : int = 25) -> []:
        """
        Выполняет поиск в Google по запросу с параметрами, которые пришли от клиента (от веб-сайта MAS).
        
        Параметры:
        --------
        message: dict
            словарь с критериями поиска вакансий от клиента
        
        maxCountOfLinks : int, optional
            максимальное количество страниц для поиска. Чем больше это число, тем дольше будет обрабатываться запрос.
            Для тестовых целей есть смысл сделать его маленьким (в пределах 10)
        
        Возвращаемое значение:
        --------
        array
            список ссылок, которые удалось достать из Google
        -------
        """
        
        user_agent = googlesearch.get_random_user_agent()
        response = googlesearch.search('Вакансии %s Гродно' % (
            message['position']), country=message['country'], stop=maxCountOfLinks, user_agent=user_agent)
        
        urls = [x for x in response]
        self.log_info("> Parsed %s items. Sending to viewer..." % len(urls))
        return urls

    def handler(self, message: dict) -> str:
        """
        Метод для работы с входящими запросами. Вызывается автоматически, когда приходит новый запрос.
        Выполняет поиск ссылок в Google по критериям запроса, после чего передаёт список ссылок агенту Viewer
        для получения информации о веб-страницах.
        
        Возарвщаемое значение:
        ------
        str
            строка (JSON) с информацией о веб-страницах и вакансиях на них
        """
        
        self.log_info("Request. Message: %s" % str(message))
        urls = self.searchInGoogle(message)
        
        response = self.sendUrlsToViewer(urls)
        self.log_info("Response. Found %s items" % (len(json.loads(response))))
        return response
