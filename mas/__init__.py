# =====> Imports <===== #
import multiprocessing

from flask import Flask, request
from flask import render_template

class AgentRunningProcess(multiprocessing.Process):
    def __init__(self, ns):
        multiprocessing.Process.__init__(self)
        self.ns = ns
        
    def run(self):
        from agents.Interactor import Interactor
        self.interactor = Interactor()
        self.ns.value = self.interactor

if __name__ == '__main__':
    processes = list()
    
    mgr = multiprocessing.Manager()
    ns = mgr.Namespace()
    
    print("[ROOT] Starting OSBRAIN thread")
    p = AgentRunningProcess(ns)
    p.daemon = False
    p.run()
    processes.append(p)
    
    print("[ROOT] OSBRAIN Interactor: %s" % str(ns.value))

    print("[ROOT] Setting up FLASK")
    app = Flask("MAS CourseWork",
        static_folder = './public',
        template_folder="./static") 

    print("[ROOT] Setting up FLASK views")

    # ======> Views <===== #
    @app.route('/')
    @app.route('/index')
    def index():
        return render_template("index.html")

    @app.route('/agent/search', methods = ['GET', 'POST'])
    def agentSearch():
        response = ns.value.request("Search: %s" % (str(request.form.values())))
        return ("Response -> %s" % (response))
    
    app.run()
