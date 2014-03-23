# -*- coding: utf-8 *-*

import time


LONG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class OrderMailSender;
    def __init__(self, orders, short=False, verbose=True):
        self._orders = orders
        self._short = short
        self._verbose = verbose

        f=open("/tmp/file.txt","w")

    def do_print(self):
        for order in self._orders:
            if not order.exists():
                self.print_order_line("Order '{0}' does not exist.\n", order.get_identifier())
                continue

            f.write("Order '{0}':".format(order.get_identifier()))
            if len(order.get_events()) == 0:
                self.print_order_line("  No registered events yet.\n")
                continue

            self.print_events(order.get_events())

    def print_order_line(self, text, *args):
        if not self._verbose:
            return
        f.write( text.format(*args))

    def print_events(self, event_list, ):
        self.print_head()
        for event in event_list:
            self.print_event(event)
        print ""

    def print_head(self):
        if self._short:
            f.write( u"  {0: ^20} | {1}".format("Date/time", "Status"))
            return

        f.write( u"  {0: ^20} | {1: ^35} | {2: ^50} | {3}".format(
            u"Date/time", "Status", "Description", "Position"))

    def print_event(self, event):
        if self._short:
            f.write( u"  {0: <20} | {1}".format(
                time.strftime(LONG_DATE_FORMAT, event.get_date()),
                event.get_text()))
            return

        f.write( u"  {0: <20} | {1: <35} | {2: <50} | {3}".format(
            time.strftime(LONG_DATE_FORMAT, event.get_date()),
            event.get_text(),
            event.get_description(),
            event.get_location()))

