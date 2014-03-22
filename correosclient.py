# -*- coding: utf-8 *-*

from urllib import urlencode
from urllib2 import urlopen

WEB_SERVICE_ENDPOINT = "https://aplicacionesweb.correos.es/localizadorenvios/track.asp"


class CorreosClient:
    def __init__(self, code):
        self._code = code

    def query(self):
        params = urlencode(self.build_params())
        response = urlopen(WEB_SERVICE_ENDPOINT, params)
        data = response.read()
        separated_data = data.split("##")
        if len(separated_data) < 2:
            return ""
        return separated_data[1].split("**", 1)[0]

    def build_query(self):
        return "{0}?{1}".format(WEB_SERVICE_ENDPOINT, self.build_params())

    def build_params(self):
        return {"numero": self._code, "accion": "LocalizaUno"}
