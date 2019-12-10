import osbrain

from agents.searcherAgent import SearcherAgent
from agents.viewerAgent import ViewerAgent

localEndPoint = "127.0.0.1:25876"

if __name__ == '__main__':
    osbrain.config['TRANSPORT'] = 'tcp'
    osbrain.config['SERIALIZER'] = 'json'

    server = osbrain.run_nameserver()

    viewer = osbrain.run_agent('Viewer', base=ViewerAgent)
    viewerAddr = viewer.bind('REP', alias='main', handler='handler')
    viewer.log_info("Viewer Agent started on %s" % str(
        osbrain.address.address_to_host_port(viewer.addr('main'))))

    searcher = osbrain.run_agent('Searcher', base=SearcherAgent)
    searcher.bind('REP', alias='main', addr=localEndPoint, handler='handler')
    searcher.log_info("Searcher Agent started on %s" % str(
        osbrain.address.address_to_host_port(searcher.addr('main'))))
    searcher.log_info("Connecting to viewer agent...")
    searcher.connect(viewerAddr, alias='viewer')
    searcher.log_info("Done. Listening for incoming connections")
