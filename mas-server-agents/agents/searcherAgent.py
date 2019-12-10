import osbrain
import json
from osbrain import Agent

import googlesearch

class SearcherAgent(Agent):

    __localAddress__ = "127.0.0.1:25565"

    def on_init(self):
        self.bind('REP', alias='main', transport='tcp', addr=self.__localAddress__, handler=self.handler)
        self.log_info("Searcher started on %s" % str(osbrain.address.address_to_host_port(self.addr('main'))))

    def searchInGoogle(self, keywords):
        print("Searching...")
        urls = []
        response = googlesearch.search('Career %s in Grodno' % (keywords), country='Belarus', stop=15)
        for i in response:
            print(i)
            urls.append(i)
        return json.dumps(urls)

    def handler(self, message):
        keywords = message['keywords']
        self.log_info("Request: %s" % keywords)
        return self.searchInGoogle(keywords)