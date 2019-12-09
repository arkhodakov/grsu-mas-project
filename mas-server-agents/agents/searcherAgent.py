import osbrain

from osbrain import Agent

class Searcher(Agent):

    __localAddress__ = "127.0.0.1:25565"

    def on_init(self):
        self.bind('REP', alias='main', transport='tcp', addr=self.__localAddress__, handler=self.handler)
        self.log_info("Searcher started on %s" % str(osbrain.address.address_to_host_port(self.addr('main'))))

    def handler(self, message):
        self.log_info("Request: %s" % message)
        return ("Requested: %s" % message)