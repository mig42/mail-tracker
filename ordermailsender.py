# -*- coding: utf-8 *-*

import sys
import time
import smtplib
import constants
import tempfile
import os
import codecs

from settings import Settings

MESSAGE_FORMAT = u"Subject: Orders info\n\n{0}"
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
        with tempfile.NamedTemporaryFile(delete=False) as mail_file:
            file_name = mail_file.name
            self.write_mail(mail_file)

        message = self.get_message(file_name)

        if self._verbose:
            print message

        self.send_mail(message)

        os.remove(file_name)

    def write_mail(self, mail_file):
        for order in self._orders:
            if not order.exists():
                self.print_order_line(
                    mail_file, "Order '{0}' does not exist.\n", order.get_identifier())
                continue

            mail_file.write(u"Order '{0}':\n".format(order.get_identifier()).encode("utf-8"))
            if len(order.get_events()) == 0:
                self.print_order_line("  No registered events yet.\n")
                continue

            self.print_events(mail_file, order.get_events())

    def print_order_line(self, mail_file, text, *args):
        if not self._verbose:
            return
        mail_file.write(text.format(*args))

    def print_events(self, mail_file, event_list):
        self.print_head(mail_file)
        if self._last_event:
            self.print_event(mail_file, event_list[-1])
            return

        for event in event_list:
            self.print_event(mail_file, event)


    def print_head(self, mail_file):
        if self._short:
            mail_file.write(u"  {0: ^20} | {1}\n".format("Date/time", "Status").encode("utf-8"))
            return
        mail_file.write( u"  {0: ^20} | {1: ^35} | {2: ^50} | {3}\n".format(
            "Date/time", "Status", "Description", "Position").encode("utf-8"))

    def print_event(self, mail_file, event):
        if self._short:
            mail_file.write(u"  {0: <20} | {1}\n".format(
                time.strftime(constants.LONG_DATE_FORMAT, event.get_date()),
                event.get_text()).encode("utf-8"))
            return
        mail_file.write(u"  {0: <20} | {1: <35} | {2: <50} | {3}\n".format(
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

    def get_message(self, mail_file_name):
        with codecs.open(mail_file_name, encoding="utf-8") as mail_file:
            return MESSAGE_FORMAT.format(mail_file.read())



