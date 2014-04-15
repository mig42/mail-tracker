# -*- coding: utf-8 *-*


import sys
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import constants
from settings import Settings


MESSAGE_FORMAT_1 = u"Subject: Orders info\n\ntext:{0}"
MESSAGE_FORMAT_2 = u"{0}\n\nhtml:{0}"
SUBJECT = "Orders info"
OUTPUT_OK = "Successfully sent email"
OUTPUT_ERROR = "Error: unable to send email"
FROM_ADDRESS = "mailtracker@gmail.com"
COMMASPACE = ", "


class PlainTextWriter:
    def __init__(self, short=False, verbose=True, last_event=False):
        self._short = short
        self._verbose = verbose
        self._last_event = last_event

    def write_orders(self, orders):
        text = []
        for order in orders:
            if not order.exists():
                self.add_line(text, "Order '{0}' does not exist.\n", order.get_identifier())
                continue

            self.add_line(text, "Order '{0}':", order.get_identifier())

            text.extend(self.get_events(order.get_events()))

        return "\n".join(text)

    def get_events(self, events):
        text = []

        if events is None or len(events) == 0:
            self.add_line(text, "  No registered events yet.")
            return text

        self.add_header(text)

        if self._last_event:
            self.add_event(text, events[-1])
            return text

        for event in events:
            self.add_event(text, event)

        return text

    def add_event(self, text, event):
        if self._short:
            self.add_line(text,
                          u"  {0: <20} | {1}\n",
                          time.strftime(constants.LONG_DATE_FORMAT,
                                        event.get_date()),
                          event.get_text())
            return

        self.add_line(text,
                      u"  {0: <20} | {1: <35} | {2: <50} | {3}\n",
                      time.strftime(constants.LONG_DATE_FORMAT, event.get_date()),
                      event.get_text(),
                      event.get_description(),
                      event.get_location())

    def add_header(self, text):
        if self._short:
            self.add_line(text, "  {0: ^20} | {1}\n", "Date/time", "Status")
            return

        self.add_line(text, "  {0: ^20} | {1: ^35} | {2: ^50} | {3}\n",
                      "Date/time", "Status", "Description", "Position")

    def add_line(self, lines_list, text, *args):
        if not self._verbose:
            return
        lines_list.append(text.format(*args).encode("utf-8"))


class HtmlWriter:
    def __init__(self, short=False, verbose=True, last_event=False):
        self._short = short
        self._verbose = verbose
        self._last_event = last_event

    def write_orders(self, orders):
        text = []
        for order in orders:
            if not order.exists():
                self.add_line(text, "Order '{0}' does not exist.<br/>", order.get_identifier())
                continue

            self.add_line(
                text, "<div style=\"display: table\">"
                      "<div style=\"display: table-caption;"
                      "text-align: center;font-weight: bold;font-size: larger\">"
                      "<p>Order '{0}'</p> </div>", order.get_identifier())

            text.extend(self.get_events(order.get_events()))
            self.add_line(text, "</div>")

        return "\n".join(text)

    def get_events(self, events):
        text = []

        if events is None or len(events) == 0:
            self.add_line(text, "  No registered events yet.")
            return text

        self.add_header(text)

        if self._last_event:
            self.add_event(text, events[-1])
            return text

        for event in events:
            self.add_event(text, event)

        return text

    def add_event(self, text, event):
        if self._short:
            self.add_line(text,
                          u"<div style=\"display: table-row\">"
                          u"<div style=\"display: table-cell;border:"
                          u" solid;border-width: thin;padding-left: 5px;"
                          u"padding-right: 5px\"><p>{0}</p></div> "
                          u"<div style=\"display: table-cell;border:"
                          u" solid;border-width: thin;padding-left: 5px;"
                          u"padding-right: 5px\"><p>{1}</p></div></div> ",
                          time.strftime(constants.LONG_DATE_FORMAT,
                                        event.get_date()), event.get_text())
            return

        self.add_line(text,
                      u"<div style=\"display: table-row\">"
                      u"<div style=\"display: table-cell;border:"
                      u" solid;border-width: thin;padding-left: 5px;"
                      u"padding-right: 5px\"><p>{0}</p></div> "
                      u"<div style=\"display: table-cell;border:"
                      u" solid;border-width: thin;padding-left: 5px;"
                      u"padding-right: 5px\"><p>{1}</p></div> "
                      u"<div style=\"display: table-cell;border:"
                      u" solid;border-width: thin;padding-left: 5px;"
                      u"padding-right: 5px\"><p>{2}</p></div> "
                      u"<div style=\"display: table-cell;border:"
                      u" solid;border-width: thin;padding-left: 5px;"
                      u"padding-right: 5px\"><p>{3}</p></div> </div> ",
                      time.strftime(constants.LONG_DATE_FORMAT, event.get_date()),
                      event.get_text(),
                      event.get_description(),
                      event.get_location())

    def add_header(self, text):
        if self._short:
            self.add_line(text, "<div style=\"display:"
                                " table-row;font-weight: bold;text-align:"
                                " center\"><div style=\"display:"
                                " table-cell;border: solid;border-width: thin;"
                                "padding-left: 5px;padding-right: 5px\">"
                                "<p><p>{0} </p> </div>"
                                "<div style=\"display:"
                                "table-cell;border: solid;border-width: thin;"
                                "padding-left: 5px;padding-right: 5px\">"
                                "<p><p> {1} </p> </div></div>",
                          "Date/time", "Status")
            return

        self.add_line(text, "<div style=\"display:"
                            " table-row;font-weight: bold;text-align:"
                            " center\"><div style=\"display:"
                            " table-cell;border: solid;border-width: thin;"
                            "padding-left: 5px;padding-right: 5px\">"
                            "<p><p>{0} </p> </div>"
                            "<div style=\"display:"
                            "table-cell;border: solid;border-width: thin;"
                            "padding-left: 5px;padding-right: 5px\">"
                            "<p><p> {1} </p> </div>"
                            "<div style=\"display:"
                            "table-cell;border: solid;border-width: thin;"
                            "padding-left: 5px;padding-right: 5px\">"
                            "<p><p> {2} </p> </div>"
                            "<div style=\"display:"
                            "table-cell;border: solid;border-width: thin;"
                            "padding-left: 5px;padding-right: 5px\">"
                            "<p><p> {3} </p> </div></div>",
                      "Date/time", "Status", "Description", "Position")

    def add_line(self, lines_list, text, *args):
        if not self._verbose:
            return
        lines_list.append(text.format(*args).encode("utf-8"))


class OrderMailSender:
    def __init__(self, orders, mails, short=False, verbose=True, last_event=False):
        self._orders = orders
        self._short = short
        self._verbose = verbose
        self._last_event = last_event
        self._toaddrs = mails

        self._settings = Settings(constants.SETTINGS_FILE)
        self._message = MIMEMultipart("alternative")
        self._message["Subject"] = SUBJECT
        self._message["From"] = FROM_ADDRESS
        self._message["To"] = COMMASPACE.join(mails)

    def execute(self):
        plain_writer = PlainTextWriter(self._short, True, self._last_event)
        plain_message = plain_writer.write_orders(self._orders)
        self._message.attach(MIMEText(plain_message, "plain", "utf-8"))

        html_writer = HtmlWriter(self._short, True, self._last_event)
        self._message.attach(MIMEText(html_writer.write_orders(self._orders), "html", "utf-8"))

        if self._verbose:
            print plain_message

        self.send_mail(self._message.as_string())

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


class OrderPrinter:
    def __init__(self, orders, short=False, verbose=True, last_event=False):
        self._orders = orders
        self._short = short
        self._verbose = verbose
        self._last_event = last_event

    def execute(self):
        plain_writer = PlainTextWriter(self._short, self._verbose, self._last_event)
        print plain_writer.write_orders(self._orders)
