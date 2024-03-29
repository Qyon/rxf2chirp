__author__ = 'Qyon'
# -*- coding: utf-8 -*-

import sys
import getopt
from przemienniki.xmlreader import PrzemiennikiXMLReader
from chirp.xmlwriter import ChirpXMLWriter

def main():
    """
    Funkcja main
    """
    try:
        input_filename, output_filename = sys.argv[1:3]
    except ValueError:
        print "Uzycie %s input.xml output.chirp" % (sys.argv[0])
        sys.exit(2)

    try:
        name_filter = sys.argv[3]
    except IndexError:
        name_filter = None

    przemienniki = PrzemiennikiXMLReader(input_filename)
    writer = ChirpXMLWriter(przemienniki)
    writer.save(output_filename, name_filter=name_filter)

if __name__ == "__main__":
    main()