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

        for block in model.content:
            items = tree.xpath(block['list'])
            print("Found %s items" % len(items))
            for item in items:
                vacancyInformation = []
                for key in block['parameters']:
                    vacancyInformation.append(self.valueOf(
                        item, block['parameters'][key],
                        func=block['functions'].get(key, None),
                        regex=block['regex'].get(key, None)))
                result.append(vacancyInformation)
        return result

    def valueOf(self, item, xpath, default=None, func=None, regex=None):
        # ----- Check for empty path
        if xpath == "" or xpath == None:
            return default
        value = item.xpath(xpath)
        if len(value) != 0:
            if func:
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
