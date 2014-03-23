# -*- coding: utf-8 *-*

import sys
import getopt

import correosparser
from orderprinter import OrderPrinter


USAGE_MESSAGE = \
    """Usage: {0} [OPTION]
  Reads a XML stream from standard input and writes it nicely."""


class Usage(Exception):
    def __init__(self, msg=USAGE_MESSAGE.format(sys.argv[0])):
        super(Usage, self).__init__()
        self.msg = msg


def read_all(stream):
    return stream.readlines()


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "sh", ["help", "short"])
        except getopt.error, msg:
            raise Usage(msg)

        short = False
        for o, a in opts:
            if o == "-h" or o == "--help":
                print USAGE_MESSAGE.format(argv[0])
                print """
    This program expects XML contents through the standard input."""
                return 0
            if o == "-s" or o == "--short":
                short = True

        text = read_all(sys.stdin)

        parser = correosparser.CorreosParser(text)
        parser.parse()

        printer = OrderPrinter(parser.get_order(), short)
        printer.do_print()

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
