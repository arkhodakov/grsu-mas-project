from explorer import Explorer
from models.data import *

url = "https://grodno.jobs.tut.by/vacancy/32165359"

print(Explorer().getContent(url, Jooble()))
