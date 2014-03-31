# -*- coding: utf-8 *-*

import json
import time
from urllib import urlencode
from urllib2 import urlopen
from urllib2 import HTTPError

import order
import event


WEB_SERVICE_ENDPOINT = "https://gls-group.eu/app/service/open/rest/EU/en/rstt001?{0}"


class NetherlandsPostClient:
    def __init__(self):
        self._parser = NetherlandsPostParser()
        pass

    def get_order(self, code):
        contents = self.query(code.get_code())
        if contents is None or contents == "":
            return order.NotFoundOrder(code)
        return self._parser.parse(contents, code)

    def query(self, code):
        url = WEB_SERVICE_ENDPOINT.format(urlencode(self.build_params(code)))
        connection = None
        try:
            connection = urlopen(url)
            return connection.read()
        except HTTPError:
            return ""
        except:
            raise
        finally:
            if connection is not None:
                connection.close()

    def build_params(self, code):
        return {"match": code}


class NetherlandsPostParser():
    def __init__(self):
        self._code = ""

    def parse(self, contents, code):
        self._code = code
        return json.loads(contents, object_hook=self.dict_to_object)

    def dict_to_object(self, dictionary):
        if "exceptionType" in dictionary:
            return order.NotFoundOrder(self._code)

        if "tuStatus" in dictionary:
            return self.process_order(dictionary["tuStatus"][0])

        if "history" in dictionary:
            return dictionary["history"]

        if "address" in dictionary:
            return self.process_event(dictionary)

        if "city" in dictionary and "countryName" in dictionary:
            return event.Location(dictionary["countryName"], dictionary["city"])

        return None

    def process_order(self, events):
        result = order.SentOrder(self._code)
        for returned_event in events:
            result.add_event(returned_event)
        return result

    def process_event(self, dict):
        location = dict["address"]
        date = time.strptime(
            dict["date"] + " " + dict["time"], "%Y-%m-%d %H:%M:%S")
        return event.Event(date, dict["evtDscr"], "", location)

