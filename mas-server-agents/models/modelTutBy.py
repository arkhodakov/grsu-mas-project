from models.model import Model


class TutByModel(Model):
    def __init__(self):
        super().__init__(
            domain="jobs.tut.by",
            name="Jobs TUT.by",
            content=[
                dict(
                    list="//div[contains(@id, 'HH-React-Root')]/div",
                    parameters=dict(
                        name=".//h1[contains(@data-qa, 'vacancy-title')]/span/text()",
                        price=".//p[contains(@class, 'vacancy-salary')]/text()[string-length(.)>0]",
                        company=".//a[contains(@itemprop, 'hiringOrganization')]/span[contains(@itemprop, 'name')]/span/text()",
                        location=".//p[span[contains(@itemprop, 'jobLocation')]]/text()"
                    ),
                    functions=dict(
                        price=lambda x: [
                            " ".join([item.replace("\xa0", "") for item in x])]
                    ),
                    regex=dict()
                ),
                dict(
                    list="//div[contains(@data-qa, 'vacancy-serp__vacancy')]",
                    parameters=dict(
                        name=".//a[contains(@data-qa, 'vacancy-serp__vacancy-title')]/text()",
                        price=".//div[contains(@data-qa, 'vacancy-serp__vacancy-compensation')]/text()[string-length(.)>0]",
                        company=".//a[contains(@data-qa, 'vacancy-serp__vacancy-employer')]/text()",
                        location=".//span[contains(@data-qa, 'vacancy-serp__vacancy-address')]/text()"
                    ),
                    functions=dict(
                        name=lambda x: [item.replace(
                            "\xa0", "") for item in x],
                        price=lambda x: [item.replace(
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
