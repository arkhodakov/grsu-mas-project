from urllib.parse import urlparse
import osbrain
import json
from osbrain import Agent

class ParserAgent(Agent):

    __localAddress__ = "127.0.0.1:25565"

    def on_init(self):
        self.bind('REP', alias='main', transport='tcp', handler=self.handler)
        self.log_info("Parser started on %s" % str(osbrain.address.address_to_host_port(self.addr('main'))))
        
    def contains(self, x, function):
        for x in self.models:
            if function(x):
                return True
        return False
           
    def parseUrl(self, url):
        parsedUrl = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUrl)
        name = domain
        
        return {
            "name": name,
            "domain": domain,
            "url": parsedUrl,
            "vacancies": [
                
            ]
        }
        
        
    def handler(self, message):
        response = []
        urls = message['urls']
        for url in urls:
            response.append(self.parseUrl(url)) 
        return json.dumps(response)