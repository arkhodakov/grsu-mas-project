import osbrain
from osbrain.address import *


class UserInteractionAgent():
    __defaultRemote__ = AgentAddress('tcp', '127.0.0.1:25876', 'REP', 'server', 'pickle')
    
    def __init__(self):
        osbrain.config['TRANSPORT'] = 'tcp'
        self.server = osbrain.run_nameserver()
        self.interactor = osbrain.run_agent("interactor")

    def request(self, message):
        self.interactor.connect(self.__defaultRemote__, alias='main')
        self.interactor.send('main', message)
        response = self.interactor.recv('main')
        self.interactor.close('main')
        return response
    
    def __str__(self):
        return "(Agent: %s)" % str(self.interactor)