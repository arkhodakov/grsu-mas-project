import osbrain

from agents.searcherAgent import Searcher

if __name__ == '__main__':
    osbrain.config['TRANSPORT'] = 'tcp'
    server = osbrain.run_nameserver()
    searcher = osbrain.run_agent('Searcher', base=Searcher)