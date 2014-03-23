# -*- coding: utf-8 *-*

import time
import xml.etree.ElementTree as ElementTree

import order
import event


class CorreosParser:
    def __init__(self, xml_text, code):
        self._xml_text = "".join(xml_text).decode('latin_1').encode('utf_8')
        self._code = code
        self._order = None

    def parse(self):
        root = ElementTree.fromstring(self._xml_text)

        root = root.find(".//Envio")
        if root is None:
            return

        code = get_text(root.find("Codigo"), "CodigoEnvio").strip()
        error_code = int(get_text(root, "CodError"))
        if error_code != 0:
            self._order = order.NotFoundOrder(self._code)
            return

        sent_order = order.SentOrder(self._code)
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

        self._order = sent_order

    def get_order(self):
        return self._order


def get_text(xml_node, child_name):
    child_node = xml_node.find(child_name)
    if child_node is None:
        return ""
    return child_node.text


