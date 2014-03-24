# -*- coding: utf-8 *-*

import time
import smtplib
import codecs

from email.header import Header
from email.message import Message

LONG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"




class OrderMailSender:
    def __init__(self, orders, mail, short=False, verbose=True):
        self._orders = orders
        self._short = short
        self._verbose = verbose
        self._username = 'mailtrackerpython'
        self._password = 'oyapulpo'
        self._toaddrs = [mail]

    def do_print(self):
        for order in self._orders:
            if not order.exists():
                self.print_order_line("Order '{0}' does not exist.\n", order.get_identifier())
                continue
            with codecs.open("/tmp/file.txt","a", "utf-8") as self._file:
                self._file.write("Order '{0}':\n".format(order.get_identifier()))
            if len(order.get_events()) == 0:
                self.print_order_line("  No registered events yet.\n")
                continue

            self.print_events(order.get_events())

    def print_order_line(self, text, *args):
        if not self._verbose:
            return
        with codecs.open("/tmp/file.txt","a", "utf-8") as self._file:
            self._file.write( text.format(*args))

    def print_events(self, event_list, ):
        self.print_head()
        for event in event_list:
            self.print_event(event)
        print ""

    def print_head(self):
        if self._short:
            with codecs.open("/tmp/file.txt","a", "utf-8") as self._file:
                self._file.write( u"  {0: ^20} | {1}\n".format("Date/time", "Status"))
            return
        with codecs.open("/tmp/file.txt","a", "utf-8") as self._file:
            self._file.write( u"  {0: ^20} | {1: ^35} | {2: ^50} | {3}\n".format(
                u"Date/time", "Status", "Description", "Position"))

    def print_event(self, event):
        if self._short:
            with codecs.open("/tmp/file.txt","a", "utf-8") as self._file:
                self._file.write( u"  {0: <20} | {1}\n".format(
                    time.strftime(LONG_DATE_FORMAT, event.get_date()),
                    event.get_text()))
            return
        with codecs.open("/tmp/file.txt","a", "utf-8") as self._file:
            self._file.write( u"  {0: <20} | {1: <35} | {2: <50} | {3}\n".format(
                    time.strftime(LONG_DATE_FORMAT, event.get_date()),
                    event.get_text(),
                    event.get_description(),
                    event.get_location()))


    def do_send_mail(self):
        with codecs.open("/tmp/file.txt","r", "utf-8") as self._file:
            self._msg = 'Subject: Order info\n\n'
            self._msg+=  self._file.read()
            #self._msg['Subject'] = Header('Order info','utf-8')
            print self._msg
        unicode(self._msg)
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.starttls()
            server.login(self._username,self._password)
            server.sendmail('mailtrackerpython@gmail.com', self._toaddrs, self._msg.encode('utf-8'))
            server.quit()
            print "Successfully sent email"
        except SMTPException:
            print "Error: unable to send email"