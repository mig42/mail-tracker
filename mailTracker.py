# -*- coding: utf-8 *-*

import sys
import getopt
import time

import xmlParser


USAGE_MESSAGE = \
    """Usage: {0} [OPTION]
    Reads a XML stream from standard input and """

LONG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


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

        parser = xmlParser.XmlParser(text)
        parser.parse()

        for readr_order in parser.get_orders():
            if not readr_order.exists():
                print "Order '{0}' does not exist.".format(readr_order.get_code())
                continue

            print "Order '{0}':".format(readr_order.get_code())
            if len(readr_order.get_events()) == 0:
                print "  No registered events yet."
                continue

            print_events(readr_order.get_events(), short)

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2


def print_events(event_list, short=False):
    print_head(short)
    for event in event_list:
        print_event(event, short)


def print_head(short=False):
    if short:
        print u"  {0: ^20} | {1}".format("Date/time", "Status")
        return

    print u"  {0: ^20} | {1: ^35} | {2: ^50} | {3}".format(
        u"Date/time", "Status", "Description", "Position")


def print_event(event, short=False):
    if short:
        print u"  {0: <20} | {1}".format(
            time.strftime(LONG_DATE_FORMAT, event.get_date()),
            event.get_text())
        return

    print u"  {0: <20} | {1: <35} | {2: <50} | {3}".format(
        time.strftime(LONG_DATE_FORMAT, event.get_date()),
        event.get_text(),
        event.get_description(),
        event.get_location())


if __name__ == "__main__":
    sys.exit(main())
