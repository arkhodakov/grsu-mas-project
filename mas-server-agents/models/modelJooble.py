from models.model import Model


class JoobleModel(Model):
    def __init__(self):
        super().__init__(
            domain="by.jooble.org",
            name="Jooble.org",
            content=[
                dict(
                    list="//div[contains(@class, 'vacancy_wrapper vacancy-js vacancy_wrapper-js')]",
                    parameters=dict(
                        name=".//h2[@class='position']//*/text()",
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
