# -*- coding: utf-8 *-*

import sys
import getopt
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

    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
