import requests
import re

from lxml import html


class Explorer():

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'referer': "https://www.google.by/"
    }

    def getContent(self, url, model) -> dict():
        result = []

        content = requests.get(url, headers=self.headers).content
        tree = html.fromstring(content)
        open('fl.html', 'wb').write(content)

        items = tree.xpath(model.content['list'])
        print("Found %s items" % len(items))
        for item in items:
            vacancyInformation = []
            for key in model.content['parameters']:
                vacancyInformation.append(self.valueOf(
                    item, model.content['parameters'][key],
                    func=model.content['functions'].get(key, None),
                    regex=model.content['regex'].get(key, None)))
            result.append(vacancyInformation)
        return result

    def valueOf(self, item, xpath, default=None, func=None, regex=None):
        # ----- Check for empty path
        if xpath == "" or xpath == None:
            return default
        value = item.xpath(xpath)
        if len(value) != 0:
            if func:
                print(value)
                value = func(value)
            value = value[0].strip('    \t\n\r')
            if regex is not None:
                try:
                    value = re.match(regex, value).groups()[0]
                except:
                    return value
            return value
        else:
            return default
