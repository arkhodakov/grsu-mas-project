import osbrain

from agents.searcherAgent import SearcherAgent
from agents.parserAgent import ParserAgent
from agents.vacancyAgent import VacancyAgent

if __name__ == '__main__':
    osbrain.config['TRANSPORT'] = 'tcp'
    osbrain.config['SERIALIZER'] = 'json'
    server = osbrain.run_nameserver()
    searcher = osbrain.run_agent('Searcher', base=SearcherAgent)
    parser = osbrain.run_agent('Parser', base=ParserAgent)
    vacancy = osbrain.run_agent('Vacancy', base=VacancyAgent)