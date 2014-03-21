# -*- coding: utf-8 *-*

import sys
import os.path
import getopt

class Usage(Exception):

    def __init__(self, msg):
        super(Usage, self).__init__()
        self.msg = msg

def main(argv = None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)

        for o, a in opts:
            if o == "-h":
                print 'Usage: {0} <file>'.format(argv[0])
                print "       file: a file containing the tracking numbers, one number per line"
                return 0


        print "Hello, world!"
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())
