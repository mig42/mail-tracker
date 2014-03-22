# -*- coding: utf-8 *-*

import sys
import getopt
import time

import xmlParser


USAGE_MESSAGE = "Usage: {0}"


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
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)

        for o, a in opts:
            if o == "-h":
                print USAGE_MESSAGE.format(argv[0])
                print """
    This program expects XML contents through the standard input."""
                return 0

        text = read_all(sys.stdin)

        parser = xmlParser.XmlParser(text)
        parser.parse()

        for readOrder in parser.get_orders():
            if not readOrder.exists():
                print "Order '{0}' does not exist.".format(readOrder.get_code())
                continue

            print "Order '{0}':".format(readOrder.get_code())
            if len(readOrder.get_events()) == 0:
                print "  No registered events yet."
                continue

            print u"  {0: ^20} | {1: ^50} | {2: ^50} | {3}".format(
                u"Date/time", "Status", "Description", "Position"
            )
            for event in readOrder.get_events():
                print u"  {0: <20} | {1: <50} | {2: <50} | {3}".format(
                    time.strftime("%Y-%M-%d %H:%M:%S", event.get_date()),
                    event.get_text(),
                    event.get_description(),
                    event.get_location())

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
