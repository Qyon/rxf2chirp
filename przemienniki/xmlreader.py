__author__ = 'Qyon'
# -*- coding: utf-8 -*-

from xml.dom import minidom
from xml.dom.minicompat import NodeList

class PrzemiennikiXMLReader(object):
    """
        Klasa odczytująca przemienniki z pliku XML
    """

    def __init__(self, filename):
        """
        :type filename: str
        """
        with open(filename, 'r') as f:
            self.dom = minidom.parse(f)

        self._read_dictionary()
        self._read_repeaters()

    def _getNodeValue(self, element, node_name):
        """
        Odczytaj zawartość textnoda zawartego w podanym elemencie
        :type element: xml.dom.minidom.Element
        :type node_name: str
        """
        type_element = element.getElementsByTagName(node_name)[0]
        item_type = type_element.firstChild.nodeValue
        return item_type

    def _read_dictionary(self):
        """
        Odczytaj wartości słownika
        """
        items = self.dom.getElementsByTagName('dictionary')[0].getElementsByTagName('item')
        self.dictionary = {}

        for item in items:
            item_type = self._getNodeValue(item, 'type')
            if not self.dictionary.get(item_type):
                self.dictionary[item_type] = {}
            node_data = dict([(node_name, self._getNodeValue(item, node_name)) for node_name in
                              ('type', 'name', 'value', 'description')])
            self.dictionary[item_type][self._getNodeValue(item, 'value')] = node_data

    def _read_repeaters(self):
        """
        Odczytaj repeatery
        """
        repeaters = self.dom.getElementsByTagName('repeaters')[0].getElementsByTagName('repeater')
        self.repeaters = {}

        for repeater in repeaters:
            repeater_id = self._getNodeValue(repeater, 'id')
            node_data = dict([(node_name, self._getNodeValue(repeater, node_name)) for node_name in
                              ('qra', 'statusInt', 'modeInt', 'bandInt', 'country', 'qth', 'activationInt')])
            try:
                for node_name in ('statusInt', 'modeInt', 'bandInt', 'activationInt'):
                    node_name_real = node_name[:-3]
                    node_data[node_name_real] = self.dictionary[node_name_real][node_data[node_name]]
                self.repeaters[repeater_id] = node_data
            except KeyError:
                # są w xmlu przemienniki których *Int pole nie ma odwzorowania w słowniku...
                continue
