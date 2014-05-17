# -*- coding: utf-8 *-*

import sys
import time
from urllib import urlencode
import urllib2
import xml.etree.ElementTree as ElementTree

import order
import event


WEB_SERVICE_ENDPOINT = "https://aplicacionesweb.correos.es/localizadorenvios/track.asp"


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
            separated_data = data.split("##")
            for chunk in separated_data:
                if chunk.startswith("<?xml"):
                    return chunk.split("**", 1)[0]
            return ""
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

    def parse(self, xml_text, code):
        _xml_text = "".join(xml_text).decode('latin_1').encode('utf_8')
        root = ElementTree.fromstring(_xml_text)

        root = root.find(".//Envio")
        if root is None:
            return

        found_code = get_text(root.find("Codigo"), "CodigoEnvio").strip()

        if found_code != code.get_code():
            print >> sys.stderr,\
                "Code mismatch: expected '{0}', found '{1}'.".format(code.get_code(), found_code)
            return order.NotFoundOrder(code)

        error_code = int(get_text(root, "CodError"))
        if error_code != 0:
            return order.NotFoundOrder(code)

        sent_order = order.SentOrder(code)
        event_list = root.find("ListaEventos")
        for xml_event in event_list.iter("Evento"):
            if len(xml_event) == 0:
                continue
            date_string = get_text(xml_event, "Fecha")
            time_string = get_text(xml_event, "Hora")
            date = time.strptime(date_string + " " + time_string, "%d/%m/%Y %H:%M:%S")
            text = get_text(xml_event, "Evento")
            description = get_text(xml_event, "DescripcionWeb")

            city = get_text(xml_event, "Unidad")
            province = get_text(xml_event, "Provincia")
            country = get_text(xml_event, "Pais")
            location = event.Location(country, city, province)
            new_event = event.Event(date, text, description, location)

            sent_order.add_event(new_event)

        return sent_order


def get_text(xml_node, child_name):
    child_node = xml_node.find(child_name)
    if child_node is None:
        return ""
    return child_node.text

