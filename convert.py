__author__ = 'Qyon'

import sys
import getopt
from przemienniki.xmlreader import PrzemiennikiXMLReader


def main():
    """
    Funkcja main
    """
    przemienniki = PrzemiennikiXMLReader('samples/rxf.xml')


if __name__ == "__main__":
    main()