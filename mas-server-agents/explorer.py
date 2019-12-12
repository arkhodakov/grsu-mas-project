import re
import requests

from lxml import html
from models.model import Model


class Explorer():
    """
    Класс 'исследователя', который проходится по странице с определённой моделью
    и вытягивает из неё данные о вакансиях.
    
    Аттрибуты:
    -------
    maxItems : int
        максимальное количество вакансий с каждого раздела веб-сатринцы
    """
    
    maxItems = 10

    def getContentFromURL(self, session: requests.Session, url: str, model: Model) -> []:
        """
        Получение списка вакансий из веб-страницы по определённому адресу (url) с использованием сессии Viewer агента
        и модели веб-сайта.
        
        Возвращаемое значение:
        -------
        array
            вакансии в виде словаря с параметрами, указанными в модели 
        """
        
        content = session.get(url).content
        tree = html.fromstring(content)

        result = []
        for block in model.content:
            items = tree.xpath(block['list'])
            type = block['type']
            counter = 0
            for item in items:
                if(counter > self.maxItems):
                    break
                vacancyInformation = {"type": type}
                for key in block['parameters']:
                    xpath = block['parameters'][key]
                    value = None
                    if xpath == "url":
                        value = url
                    else:
                        value = self.valueOf(
                            item, xpath,
                            func=block['functions'].get(key, None),
                            regex=block['regex'].get(key, None))
                    vacancyInformation.update({
                        key: value
                    })
                result.append(vacancyInformation)
                counter += 1
        return result

    def valueOf(self, item: html.HtmlElement, xpath: str, default: str = None, regex: str = None, func=None) -> str:
        """
        Плучение информации из элемента списка вакансий по определённому локатору (xpath)
        с применением функций парсинга (func) и регулярных выражений (regex).
        
        Возвращаемое значение:
        -------
        str
            значение элемента по локатору
        """
        
        if xpath == "" or xpath == None:
            return default
        value = item.xpath(xpath)
        if len(value) != 0:
            if func:
                value = func(value)
            value = value[0].strip('    \t\n\r')
            if regex is not None:
                try:
                    value = re.match(regex, value).groups()[0]
                except:
                    return value
            return value
        else:
            return default
