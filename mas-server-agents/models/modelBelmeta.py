from models.model import Model


class BelmetaModel(Model):
    def __init__(self):
        super().__init__(
            domain="belmeta.com",
            name="Belmeta",
            content=[
                dict(
                    list="//article[contains(@class, 'job')]",
                    parameters=dict(
                        name=".//h2[@class='title']/a/text()",
                        price=".//div[@class='salary']/text()",
                        company=".//div[@class='company']/text()",
                        location=".//div[@class='region']/text()"
                    ),
                    functions=dict(
                        price=lambda x: [
                            " ".join([item.replace("\xa0", "") for item in x])]
                    ),
                    regex=dict()
                )
            ]
        )
