# -*- coding: utf-8 *-*

import sys
import getopt
import os.path
import codecs

from correosclient import CorreosClient
from correosparser import CorreosParser
from orderprinter import OrderPrinter
from codeparser import CodeParser
from ordermailsender import OrderMailSender

USAGE_MESSAGE = \
    """Usage: {0} <code> | -f <file>
  Queries the correos.es web service to retrieve an order status in XML format"""
HELP_MESSAGE = """Receives a list of codes as arguments, or a file containing them.
  -f:   Specifies a file in which tracking codes will be found.
  -q:   Supresses superfluous output messages."""


class Usage(Exception):
    def __init__(self, msg=USAGE_MESSAGE.format(sys.argv[0])):
        super(Usage, self).__init__()
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "sqhf:m:", ["help", "short","mail"])
        except getopt.error, msg:
            raise Usage(msg)

        short = False
        code_file = None
        verbose = True
        for key, value in opts:
            if key == "-h" or key == "--help":
                print USAGE_MESSAGE.format(argv[0])
                print HELP_MESSAGE
                return 0
            if key == "-s" or key == "--short":
                short = True
            if key == "-q":
                verbose = False
            if key == "-f":
                if value is None or value == "":
                    raise Usage("No file was specified.")
                if not os.path.isfile(value):
                    raise Usage("File {0} couldn't be found.".format(value))
                code_file = value
            if key == "-m" or key == "--mail":
                if value is None or value == "":
                    raise Usage("No mail was specified.")
                mail = value


        codes = []
        for code in get_args(args, code_file):
            if verbose:
                print "Processing {0}...".format(code.get_identifier())
            client = CorreosClient(code)

            parser = CorreosParser(client.query(), code)
            try:
                parser.parse()
                codes.append(parser.get_order())
            except:
                pass

        if verbose:
            print ""

        if mail == "":
            printer = OrderPrinter(codes, short, verbose)
            printer.do_print()
        else:
            with codecs.open("/tmp/file.txt","w", "utf-8") as file:
                file.write(" ")
            printer = OrderMailSender (codes, mail, short, verbose)
            printer.do_print()
            printer.do_send_mail()



    except Usage, err:
        print >> sys.stderr, err.msg
        print >> sys.stderr, "For help use --help"
        return 2


def get_args(args, path):
    if path is not None:
        lines = get_args_from_file(path)
    else:
        lines = args
    parser = CodeParser(lines)
    return parser.get_codes()


def get_args_from_file(path):
    with open(path, 'r') as file:
        result = []
        line = file.readline()
        while line != "":
            result.append(line)
            line = file.readline()
        return result


if __name__ == "__main__":
    sys.exit(main())