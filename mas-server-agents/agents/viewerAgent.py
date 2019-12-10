import json
import types
import osbrain

from osbrain import Agent
from urllib.parse import urlparse
from explorer import Explorer
from models.modelTutBy import TutByModel


class ViewerAgent(Agent):

    models = [
        TutByModel()
    ]

    def __contains__(self, x, function):
        for x in self.models:
            if function(x):
                return x
        return None

    def on_init(self):
        self.explorer = Explorer()

    def processUrlLink(self, url):
        parsedUrl = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsedUrl)

        info = {
            "name": None,
            "domain": domain,
            "url": url,
            "vacancies": []
        }

        model = self.__contains__(domain, lambda x: x.domain in domain)
        if model is not None:
            self.log_info("Applying model to %s" % (url))
            info['name'] = model.name
            info['vacancies'].extend(self.explorer.getContent(url, model))
            

        return info

    def handler(self, message):
        return json.dumps(self.processUrlLink(message))
