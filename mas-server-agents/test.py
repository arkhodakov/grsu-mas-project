from explorer import Explorer
from models.modelTutBy import TutByModel
from models.modelBelmeta import BelmetaModel
from models.modelJooble import JoobleModel

print(Explorer().getContent(
    "https://by.jooble.org/%D0%B2%D0%B0%D0%BA%D0%B0%D0%BD%D1%81%D0%B8%D0%B8-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82-c%23-(asp.net)/%D0%93%D1%80%D0%BE%D0%B4%D0%BD%D0%BE", JoobleModel()))
