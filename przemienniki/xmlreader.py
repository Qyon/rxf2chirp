__author__ = 'Qyon'
# -*- coding: utf-8 -*-

from xml.dom import minidom
from xml.dom.minidom import Element


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

    def _getNodeValue(self, parent_element, node_name):
        """
        Odczytaj zawartość textnoda zawartego w podanym elemencie
        :type element: xml.dom.minidom.Element
        :type node_name: str
        """
        elements = parent_element.getElementsByTagName(node_name)
        if len(elements) == 1:
            child_element = elements[0]
            element_value = child_element.firstChild.nodeValue
        elif len(elements) > 1:
            element_value = []
            for element in elements:
                val = dict([(a_name, a_value.nodeValue) for (a_name, a_value) in element._attrs.items()])
                val['value'] = element.firstChild.nodeValue
                element_value.append(val)
        else:
            element_value = None
        return element_value

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
        repeaters_cnt = 0
        for repeater in repeaters:
            try:
                repeater_id = self._getNodeValue(repeater, 'id')
                node_data = dict([(node_name, self._getNodeValue(repeater, node_name)) for node_name in
                                  ('qra', 'statusInt', 'modeInt', 'bandInt', 'country', 'qth', 'activationInt', 'qrg', 'ctcss')])

                try:
                    for node_name in ('statusInt', 'modeInt', 'bandInt', 'activationInt'):
                        node_name_real = node_name[:-3]
                        #			<ctcss type="rx">127.3</ctcss>
                        #           <ctcss type="tx">127.3</ctcss>
                        node_data[node_name_real] = self.dictionary[node_name_real][node_data[node_name]]
                    self.repeaters[repeater_id] = node_data
                except KeyError:
                    # są w xmlu przemienniki których *Int pole nie ma odwzorowania w słowniku...
                    continue

                repeaters_cnt += 1
            except Exception as e:
                print e
