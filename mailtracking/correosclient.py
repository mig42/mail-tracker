# -*- coding: utf-8 *-*

import sys
import time
from urllib import urlencode
import urllib2
from BeautifulSoup import BeautifulSoup

import order
import event


WEB_SERVICE_ENDPOINT = "http://aplicacionesweb.correos.es/localizadorenvios/track.asp"


class CorreosClient:
    def __init__(self):
        self._parser = CorreosParser()

    def get_order(self, code):
        content = self.query(code.get_code())
        if content is None or content == "":
            return order.NotFoundOrder(code)
        return self._parser.parse(content, code)

    def query(self, code):
        connection = None
        params = urlencode(self.build_params(code))
        try:
            connection = urllib2.urlopen(WEB_SERVICE_ENDPOINT, params)
            data = connection.read()
            return data
        except urllib2.URLError:
            return ""
        except:
            raise
        finally:
            if connection is not None:
                connection.close()

    def build_params(self, code):
        return {"numero": code, "accion": "LocalizaUno"}


class CorreosParser:
    def __init__(self):
        pass

    def parse(self, html_text, code):
        soup = BeautifulSoup(html_text)

        if soup is None:
            return

        found_code = self.find_code(soup)

        if found_code != code.get_code():
            print >> sys.stderr,\
                "Code mismatch: expected '{0}', found '{1}'.".format(code.get_code(), found_code)
            return order.NotFoundOrder(code)

        #error_code = int(get_text(root, "CodError"))
        #if error_code != 0:
        #    return order.NotFoundOrder(code)

        sent_order = order.SentOrder(code)
        event_list = soup.findAll('table')[0].findAll('tr')[2:]
        
        try:
            for html_event in event_list:
                if len(html_event) == 0:
                    continue
                date_string = html_event.findAll('td')[0].contents
                date = time.strptime(date_string[0], "\r\t\t\t\t%d/%m/%Y")
                description_html = html_event.findAll('td')[1]
                description = description_html.span['title']
                text =description_html.contents[1].contents[0].split("\r")[0]
                new_event = event.Event(date, text, description, None)

                sent_order.add_event(new_event)
        except:
            return order.NotFoundOrder(code)

        return sent_order

    def find_code(self, soup):
        try:
            code = soup.findAll('td')[0].contents[0].split(';')[2]
        except:
            return ""
    
        return code
    
def get_text(xml_node, child_name):
    child_node = xml_node.find(child_name)
    if child_node is None:
        return ""
    return child_node.text

