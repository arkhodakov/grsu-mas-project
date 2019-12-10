# =====> Imports <===== #
import multiprocessing
import json

from flask import Flask, render_template, request

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
    app = Flask("MAS CourseWork",
        static_folder = './public',
        template_folder="./static") 


    # =====> Routes <====== #
    print("[ROOT] Setting up FLASK views")    
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template("index.html")

    @app.route('/agent/search', methods = ['GET', 'POST'])
    def agentSearch():
        data = request.get_json()
        print("Request: %s" % data)
        response = ns.value.request(data)
        return response


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
    
    app.run()