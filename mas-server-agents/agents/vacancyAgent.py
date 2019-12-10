import osbrain
import json
from osbrain import Agent

# =====> Models <===== #
from models.modelTutBy import TutByModel

class VacancyAgent(Agent):

    __localAddress__ = "127.0.0.1:25565"
    
    models = [
        TutByModel()
    ]
    
    def on_init(self):
        self.bind('REP', alias='main', transport='tcp', handler=self.handler)
        self.log_info("Vacancy Agent started on %s" % str(osbrain.address.address_to_host_port(self.addr('main'))))
        

    def format(self, url, domain):
        model = self.contains(url)
        
    def handler(self, message):
        response = []
        urls = message['urls']
        for url in urls:
            response.append(self.parseUrl(url)) 
        return json.dumps(response)