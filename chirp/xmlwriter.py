# -*- coding: utf-8 -*-
__author__ = 'Qyon'

from xml.dom import minidom
from xml.dom.minidom import Element, Document
import re

class ChirpXMLWriter(object):
    """
    Klasa zapisująca przemienniki do pliku kompatybilnego z CHIRP http://chirp.danplanet.com/projects/chirp/wiki/Home
    """
    def __init__(self, przemienniki):
        """
        :type przemienniki: PrzemiennikiXMLReader
        """
        self.przemienniki = przemienniki

    def save(self, filename, include_inactive=False, name_filter=None):
        """
        :type filename: str
        """
        if name_filter:
            name_filter = name_filter.replace('?', '([\w]+)')
            name_filter = name_filter.replace('*', '(.*)')
            name_filter = re.compile(name_filter)

        xml = minidom.getDOMImplementation().createDocument(None, 'radio', None)
        assert isinstance(xml, Document)
        radio = xml.getElementsByTagName('radio')[0]
        assert isinstance(radio, Element)
        radio.setAttribute('version', '0.1.1')
        memories = xml.createElement('memories')

        location_counter = 0
        repeaters_list = self.przemienniki.repeaters.values()
        repeaters_list = sorted(repeaters_list, key=lambda r: r['qra'])
        for repeater in repeaters_list:

            if not include_inactive and repeater['status']['name'] != 'WORKING':
                continue
            if name_filter and not re.match(name_filter, repeater['qra']):
                continue

            memory = xml.createElement('memory')
            memory.setAttribute('location', str(location_counter))

            shortName = xml.createElement('shortName')
            shortName.appendChild(xml.createTextNode(repeater['qra'][:6]))
            memory.appendChild(shortName)

            longName = xml.createElement('longName')
            #longName.appendChild(xml.createTextNode(repeater['qth'])) #wywala sie
            longName.appendChild(xml.createTextNode(repeater['qra']))
            memory.appendChild(longName)

            frequency = xml.createElement('frequency')
            qrgs = repeater['qrg']
            freq = '0'
            for qrg in qrgs:
                if qrg['type'] == 'rx':
                    freq = qrg['value']
            frequency.appendChild(xml.createTextNode(freq))
            frequency.setAttribute('units', 'MHz')
            memory.appendChild(frequency)


            #stubs
            for i in (('rtone', 'repeater'), ('ctone', 'ctcss'), ('dtcs', 'dtcs'), ):
                squelch = xml.createElement('squelch')
                squelch.setAttribute('id', i[0])
                squelch.setAttribute('type', i[1])

                if i[0] != 'dtcs':
                    tone = xml.createElement('tone')
                    tone.appendChild(xml.createTextNode('88.5'))
                    squelch.appendChild(tone)
                else:
                    code = xml.createElement('code')
                    code.appendChild(xml.createTextNode('023'))
                    squelch.appendChild(code)

                    polarity = xml.createElement('polarity')
                    polarity.appendChild(xml.createTextNode('NN'))
                    squelch.appendChild(polarity)


                memory.appendChild(squelch)

            squelchSetting = xml.createElement('squelchSetting')
            memory.appendChild(squelchSetting)

            duplex = xml.createElement('duplex')
            duplex.appendChild(xml.createTextNode('none'))
            memory.appendChild(duplex)

            offset = xml.createElement('offset')
            offset.setAttribute('units', 'MHz')
            offset.appendChild(xml.createTextNode('0.0'))
            memory.appendChild(offset)

            mode = xml.createElement('mode')
            #mode.appendChild(xml.createTextNode(repeater['mode']['name']))
            mode.appendChild(xml.createTextNode('FM'))
            memory.appendChild(mode)
            #end stubs



            #stubs
            tuningStep = xml.createElement('tuningStep')
            tuningStep.setAttribute('units', 'kHz')
            tuningStep.appendChild(xml.createTextNode('1.0'))
            memory.appendChild(tuningStep)
            #end stubs



            memories.appendChild(memory)
            location_counter += 1

        radio.appendChild(memories)

        banks = xml.createElement('banks')
        radio.appendChild(banks)
        #print xml.toprettyxml();
        with open(filename, 'w') as f:
            f.write(radio.toxml('utf-8'))