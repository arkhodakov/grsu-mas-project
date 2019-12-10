from explorer import Explorer
from models.modelTutBy import TutByModel

print(Explorer().getContent(
    "https://jobs.tut.by/vacancy/33332479", TutByModel()))
