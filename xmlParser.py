# -*- coding: utf-8 *-*

import sys


class XmlParser:
    def __init__(self, xml_text):
        self._xml_text = "".join(xml_text).decode('latin_1').encode('utf_8')

    def parse(self):
        print "Read:\n---\n{0}\n---".format(self._xml_text)
