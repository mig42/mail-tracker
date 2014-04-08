# -*- coding: utf-8 *-*

import getopt
import os.path

from correosclient import CorreosClient
from netherlandspostclient import NetherlandsPostClient
from codeparser import CodeParser
from ordermailsender import *


USAGE_MESSAGE = \
    """Usage: {0} [CODE]... [OPTION]...
  Queries post companies web services to retrieve orders status """
HELP_MESSAGE = """Receives a list of codes as arguments, or a file containing them:
   -f <file>            Specifies a file in which tracking codes will be found.
   -q                   Supresses superfluous output messages.
   -m, --mail <mail1,mail2,...>
                        Specifies a mail to send tracking information
   -l, --last-event     Just print last order event"""

clients = [CorreosClient(), NetherlandsPostClient()]


class Usage(Exception):
    def __init__(self, msg=USAGE_MESSAGE.format(sys.argv[0])):
        super(Usage, self).__init__()
        self.msg = msg


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "sqhf:m:l", ["help", "short", "mail","last-event"])
        except getopt.error, msg:
            raise Usage(msg)

        short = False
        code_file = None
        verbose = True
        mail = ""
        last_event = False

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
            if key == "-l" or key == "--last-event":
                last_event = True

        orders = []
        for code in get_args(args, code_file):
            if verbose:
                print "Processing {0}...".format(code.get_identifier())
            try:
                orders.append(get_order(code))
            except:
                raise

        for order in orders:
            if order.exists():
                order.reorder_events()

        if verbose:
            print ""

        if mail == "":
            printer = OrderPrinter(orders, short, verbose, last_event)
        else:
            printer = OrderMailSender(orders, parse_addresses(mail), short, verbose, last_event)
        printer.execute()

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


def parse_addresses(email_string):
    return email_string.replace(" ", "").split(",")


def get_order(code):
    order = None
    for client in clients:
        order = client.get_order(code)
        if order.exists():
            return order
    return order


if __name__ == "__main__":
    sys.exit(main())
