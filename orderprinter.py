# -*- coding: utf-8 *-*

import time


LONG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class OrderPrinter:
    def __init__(self, orders):
        self._orders = orders

    def do_print(self, short=False):
        for order in self._orders:
            if not order.exists():
                print "Order '{0}' does not exist.\n".format(order.get_code())
                continue

            print "Order '{0}':".format(order.get_code())
            if len(order.get_events()) == 0:
                print "  No registered events yet.\n"

                continue

            print_events(order.get_events(), short)


def print_events(event_list, short=False):
    print_head(short)
    for event in event_list:
        print_event(event, short)
    print ""


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
