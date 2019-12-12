from models.model import Model


"""
Большой файл со всеми моделями, используемыми агентом Viewer для работы с веб-страницами и сайтами.
Каждая модель содержит список определённых параметров:

domain : str
    доменное имя, по которому потом осуществляется поиск модели
    
name : str
    читаемое имя веб-сайта / компании, нужно для графического представления на сайте
    
blocked : boolean
    флаг, определяющий был ли забанен веб-сайт (есть веб-сайты, которые сами парсят данные с других веб-сайтов)
    
content : array <dict>
    список разделов веб-страницы, из которых есть смысл парсить вакансии
    
    > list : str
        локатор для списка вакансий
    
    > type : str
        тип вакансии (main - главная, related - дополнительные вакансии, относящиеся к искомой теме)
        
    > parameters : dict
        параметры вакансии и локаторы, по которым вытаскиваются значения
        
        > name : str
            наименование вакансии
        
        > image : str
            ссылка на изображение компании / вакансии
            
        > salary : str
            обещанная З/П
            
        > company : str
            наименование компании
            
        > location : str
            расположение компании
    
    > function : dict
        функции для работы с параметрами. Выполняются первыми - перед regex
        
    > regex : dict
        регулярные выражения для параметров
"""

class TutBy(Model):
    def __init__(self):
        super().__init__(
            domain="jobs.tut.by",
            name="Jobs TUT.by",
            blocked=False,
            content=[
                dict(
                    list="//div[contains(@id, 'HH-React-Root')]/div",
                    type='main',
                    parameters=dict(
                        name=".//h1[contains(@data-qa, 'vacancy-title')]/span/text()",
                        image=".//a[@class='vacancy-company-logo']/img/@src",
                        salary=".//p[contains(@class, 'vacancy-salary')]/text()[string-length(.)>0]",
                        company=".//a[contains(@itemprop, 'hiringOrganization')]/span[contains(@itemprop, 'name')]/span/text()",
                        location=".//p[span[contains(@itemprop, 'jobLocation')]]/text()",
                        link="url"
                    ),
                    functions=dict(
                        salary=lambda x: [
                            " ".join([item.replace("\xa0", "") for item in x])]
                    ),
                    regex=dict()
                ),
                dict(
                    list="//div[@data-qa='vacancy-serp__vacancy']",
                    type='related',
                    parameters=dict(
                        name=".//a[contains(@data-qa, 'vacancy-serp__vacancy-title')]/text()",
                        salary=".//div[contains(@data-qa, 'vacancy-serp__vacancy-compensation')]/text()[string-length(.)>0]",
                        company=".//a[contains(@data-qa, 'vacancy-serp__vacancy-employer')]/text()",
                        location=".//span[contains(@data-qa, 'vacancy-serp__vacancy-address')]/text()",
                        link=".//a[contains(@data-qa, 'vacancy-serp__vacancy-title')]/@href"
                    ),
                    functions=dict(
                        name=lambda x: [item.replace(
                            "\xa0", "") for item in x],
                        salary=lambda x: [item.replace(
                            "\xa0", "") for item in x],
                        company=lambda x: [item.replace(
                            "\xa0", "") for item in x],
                        location=lambda x: [item.replace(
                            "\xa0", "") for item in x],
                    ),
                    regex=dict()
                )
            ]
        )


class Jooble(Model):
    def __init__(self):
        super().__init__(
            domain="by.jooble.org",
            name="Jooble.org",
            blocked=False,
            content=[
                dict(
                    list="//div[contains(@class, 'vacancy_wrapper vacancy-js vacancy_wrapper-js')]",
                    type="main",
                    parameters=dict(
                        name=".//h2[@class='position']//*/text()",
                        link=".//a[@class='link-position job-marker-js visited']/@href",
                        salary=".//span[@class='salary']/text()",
                        company=".//span[@class='gray_text company-name']/text()",
                        location=".//span[@class='date_location__region']/text()"
                    ),
                    functions=dict(
                        name=lambda x: [
                            "".join(x)
                        ],
                        salary=lambda x: [
                            " ".join([item.replace("\xa0", "") for item in x])]
                    ),
                    regex=dict()
                )
            ]
        )


class Trudbox(Model):
    def __init__(self):
        super().__init__(
            domain="trudbox.by",
            name="Trudbox",
            blocked=False,
            content=[
                dict(
                    list="//div[@class='col-md-6 center inverse_right']/div[@class='simple-results']/div[@class='items']/div[@class='block result hightlighted favorites-container']",
                    type="main",
                    parameters=dict(
                        name=".//div[@itemprop='title']/text()",
                        description=".//div[@itemprop='description']/text()",
                        link=".//a[@class='hline_4 company text-info i-house']/@href",
                        salary=".//span[@class='salary']/text()",
                        company=".//span[@itemprop='hiringOrganization']/span/text()",
                        location=".//span[@itemprop='addressLocality']/text()"
                    ),
                    functions=dict(),
                    regex=dict()
                )
            ]
        )


# ====> Blocked <==== #
class Belmeta(Model):
    def __init__(self):
        super().__init__(
            domain="belmeta.com",
            blocked=True
        )
