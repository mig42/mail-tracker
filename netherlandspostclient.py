# -*- coding: utf-8 *-*

from urllib import urlencode
from urllib2 import urlopen

WEB_SERVICE_ENDPOINT = "https://gls-group.eu/app/service/open/rest/EU/en/rstt001"


class NetherlandsPostClient:
    def __init__(self):
        self._parser = NetherlandsPostParser()
        pass

    def get_order(self, code):
        contents = self.query(code)
        if contents is None or contents == "":
            return None
        return self._parser.parse(contents, code)

    def query(self, code):
        params = urlencode(self.build_params(code))
        with urlopen(WEB_SERVICE_ENDPOINT, params) as response:
            return response.read()

    def build_params(self, code):
        return {"match": code}


class NetherlandsPostParser:

    def __init__(self):
        pass

    def parse(self, contents, code):
        pass
