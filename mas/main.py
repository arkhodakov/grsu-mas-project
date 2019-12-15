# =====> Imports <===== #
import multiprocessing
import json

from flask import Flask, Blueprint, render_template, request

class AgentRunningProcess(multiprocessing.Process):
    def __init__(self, ns):
        multiprocessing.Process.__init__(self)
        self.ns = ns
        
    def run(self):
        from agents.userInteractionAgent import UserInteractionAgent
        self.agent = UserInteractionAgent()
        self.ns.value = self.agent

if __name__ == '__main__':
    # ======> Flask <====== #
    print("[ROOT] Setting up FLASK")
    app = Flask("MAS Course Work",
        static_folder = './public',
        template_folder="./static") 


    # =====> Routes <====== #
    print("[ROOT] Setting up FLASK views")
    indexBlueprint = Blueprint('index', __name__)
    
    @indexBlueprint.route('/')
    @indexBlueprint.route('/index')
    def index():
        return render_template("index.html")
    app.register_blueprint(indexBlueprint)

    apiBlueprint = Blueprint('api', __name__)
    
    @apiBlueprint.route('/agent/search', methods=['POST'])
    def agentSearch():
        data = ns.value.request(request.get_json())
        return data
    app.register_blueprint(apiBlueprint)

    # ======> osBrain <====== #
    processes = list()
    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    
    print("[ROOT] Starting OSBRAIN thread")
    p = AgentRunningProcess(ns)
    p.daemon = False
    p.run()
    processes.append(p)

    print("[ROOT] OSBRAIN Interactor: %s" % str(ns.value))
    
    app.config.from_object('configurations.DevelopmentConfig')
    app.run()
