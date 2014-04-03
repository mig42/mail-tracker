# -*- coding: utf-8 *-*


import sys
import time
import smtplib
import constants
import tempfile
import os
import codecs


from settings import Settings


MESSAGE_FORMAT_1 = u"Subject: Orders info\n\ntext:{0}"
MESSAGE_FORMAT_2 = u"{0}\n\nhtml:{0}"
OUTPUT_OK = "Successfully sent email"
OUTPUT_ERROR = "Error: unable to send email"


class OrderMailSender:
    def __init__(self, orders, mails, short=False, verbose=True, last_event=False):
        self._orders = orders
        self._short = short
        self._verbose = verbose
        self._last_event = last_event

        self._settings = Settings(constants.SETTINGS_FILE)

        self._toaddrs = mails

    def flush_output(self):
        with tempfile.NamedTemporaryFile(delete=False) as text_mail_file:
            text_file_name = text_mail_file.name
            self.text_write_mail(text_mail_file)

        with tempfile.NamedTemporaryFile(delete=False) as html_mail_file:
            html_file_name = html_mail_file.name
            self.html_write_mail(html_mail_file)

        message = self.get_message(text_file_name, html_file_name)

        if self._verbose:
            print message

        self.send_mail(message)

        os.remove(text_file_name)

    def text_write_mail(self, text_mail_file):
        for order in self._orders:
            if not order.exists():
                self.text_print_order_line(
                    text_mail_file, "Order '{0}' does not exist.\n", order.get_identifier())
                continue

            text_mail_file.write(u"Order '{0}':\n".format(order.get_identifier()).encode("utf-8"))
            if len(order.get_events()) == 0:
                self.text_print_order_line("  No registered events yet.\n")
                continue

            self.text_print_events(text_mail_file, order.get_events())

    def html_write_mail(self, html_mail_file):
        for order in self._orders:
            if not order.exists():
                self.html_print_order_line(
                    html_mail_file, "Order '{0}' does not exist.\n", order.get_identifier())
                continue

            html_mail_file.write(u"Order '{0}':\n".format(order.get_identifier()).encode("utf-8"))
            if len(order.get_events()) == 0:
                self.html_print_order_line("  No registered events yet.\n")
                continue

            self.html_print_events(html_mail_file, order.get_events())

    def text_print_order_line(self, text_mail_file, text, *args):
        if not self._verbose:
            return
        text_mail_file.write(text.format(*args))

    def html_print_order_line(self, html_mail_file, text, *args):
        if not self._verbose:
            return
        html_mail_file.write(text.format(*args))

    def text_print_events(self, text_mail_file, event_list):
        self.text_print_head(text_mail_file)
        if self._last_event:
            self.text_print_event(text_mail_file, event_list[-1])
            return

        for event in event_list:
            self.text_print_event(text_mail_file, event)

    def html_print_events(self, html_mail_file, event_list):
        self.html_print_head(html_mail_file)
        if self._last_event:
            self.html_print_event(html_mail_file, event_list[-1])
            return

        for event in event_list:
            self.html_print_event(html_mail_file, event)

    def text_print_head(self, text_mail_file):
        if self._short:
            text_mail_file.write(u"  {0: ^20} | {1}\n".format("Date/time", "Status").encode("utf-8"))
            return
        text_mail_file.write( u"  {0: ^20} | {1: ^35} | {2: ^50} | {3}\n".format(
            "Date/time", "Status", "Description", "Position").encode("utf-8"))

    def html_print_head(self, html_mail_file):
        if self._short:
            html_mail_file.write(u"  {0: ^20} | {1}\n".format("Date/time", "Status").encode("utf-8"))
            return
        html_mail_file.write( u"  {0: ^20} | {1: ^35} | {2: ^50} | {3}\n".format(
            "Date/time", "Status", "Description", "Position").encode("utf-8"))

    def text_print_event(self, text_mail_file, event):
        if self._short:
            text_mail_file.write(u"  {0: <20} | {1}\n".format(
                time.strftime(constants.LONG_DATE_FORMAT, event.get_date()),
                event.get_text()).encode("utf-8"))
            return
        text_mail_file.write(u"  {0: <20} | {1: <35} | {2: <50} | {3}\n".format(
            time.strftime(constants.LONG_DATE_FORMAT, event.get_date()),
            event.get_text(),
            event.get_description(),
            event.get_location()).encode("utf-8"))

    def html_print_event(self, html_mail_file, event):
        if self._short:
            html_mail_file.write(u"  {0: <20} | {1}\n".format(
                time.strftime(constants.LONG_DATE_FORMAT, event.get_date()),
                event.get_text()).encode("utf-8"))
            return
        html_mail_file.write(u"  {0: <20} | {1: <35} | {2: <50} | {3}\n".format(
            time.strftime(constants.LONG_DATE_FORMAT, event.get_date()),
            event.get_text(),
            event.get_description(),
            event.get_location()).encode("utf-8"))

    def send_mail(self, message):
        server = smtplib.SMTP(self._settings.smtp_server)
        try:
            server.starttls()
            server.login(self._settings.username, self._settings.password)
            server.sendmail(
                self._settings.username, self._toaddrs, message.encode("utf-8"))
            if self._verbose:
                print OUTPUT_OK
        except smtplib.SMTPException:
            print >> sys.stderr, OUTPUT_ERROR
        finally:
            if server is not None:
                server.quit()

    def get_message(self, text_file_name, html_file_name):
        with codecs.open(text_file_name, encoding="utf-8") as text_mail_file:
            message = MESSAGE_FORMAT_1.format(text_mail_file.read())

        with codecs.open(html_file_name, encoding="utf-8") as html_mail_file:
            return MESSAGE_FORMAT_2.format(message, html_mail_file.read())