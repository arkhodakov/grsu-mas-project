import osbrain
import json
from osbrain import Agent

import googlesearch

class SearcherAgent(Agent):

    def searchInGoogle(self, keywords):
        result = []
        response = googlesearch.search('Вакансии %s Гродно' % (keywords), country='Belarus', stop=15)
        for url in response:
            self.send('viewer', url)
            result.append(self.recv('viewer'))
        return json.dumps(result)

    def handler(self, message):
        keywords = message['keywords']
        self.log_info("Request. Keywords: %s" % keywords)
        return self.searchInGoogle(keywords)
