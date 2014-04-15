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

INFO_LINE_HTML = "<div style=\"font-style: italic;\">Order '{0}'{1}</div>"

TABLE_START_HTML = "<div style=\"display: table\">"
TABLE_END_HTML = "</div>"

TABLE_CAPTION_HTML = """
<div style="display: table-caption; text-align: center;font-weight: bold;font-size: larger">
  <p>{0}</p>
</div>"""

TABLE_ROW_HTML = "<div style=\"display: table-row\">"
TABLE_TITLE_ROW_HTML = "<div style=\"display: table-row;font-weight: bold;text-align: center\">"
TABLE_END_ROW_HTML = "</div>"

TABLE_CELL_HTML = u"""
<div style="display: table-cell;border: solid;border-width: thin;padding-left:5px;padding-right:5px">
  <p>{0}</p>
</div>"""


class PlainTextWriter:
    def __init__(self, short=False, verbose=True, last_event=False):
        self._short = short
        self._verbose = verbose
        self._last_event = last_event
        self._text = []

    def write_orders(self, orders):
        self._text = []
        for order in orders:
            if not order.exists():
                self.add_line("Order '{0}' does not exist.\n", order.get_identifier())
                continue

            self.add_line("Order '{0}':", order.get_identifier())

            self.add_events(order.get_events())

        return "\n".join(self._text)

    def add_events(self, events):

        if events is None or len(events) == 0:
            self.add_line("  No registered events yet.")
            return

        self.add_header()

        if self._last_event:
            self.add_event(events[-1])
            return

        for event in events:
            self.add_event(event)

        return

    def add_event(self, event):
        if self._short:
            self.add_line(u"  {0: <20} | {1}\n",
                          time.strftime(constants.LONG_DATE_FORMAT,
                                        event.get_date()),
                          event.get_text())
            return

        self.add_line(u"  {0: <20} | {1: <35} | {2: <50} | {3}\n",
                      time.strftime(constants.LONG_DATE_FORMAT, event.get_date()),
                      event.get_text(),
                      event.get_description(),
                      event.get_location())

    def add_header(self):
        if self._short:
            self.add_line("  {0: ^20} | {1}\n", "Date/time", "Status")
            return

        self.add_line("  {0: ^20} | {1: ^35} | {2: ^50} | {3}\n",
                      "Date/time", "Status", "Description", "Position")

    def add_line(self, text, *args):
        if not self._verbose:
            return
        self._text.append(text.format(*args).encode("utf-8"))


class HtmlWriter:
    def __init__(self, short=False, verbose=True, last_event=False):
        self._short = short
        self._verbose = verbose
        self._last_event = last_event
        self._text = []

    def write_orders(self, orders):
        self._text = []
        for order in orders:
            if not order.exists():
                self.add_line(TABLE_CAPTION_HTML, order.get_identifier(), " does not exist")
                continue

            self.begin_table()
            self.add_line(TABLE_CAPTION_HTML, order.get_identifier())

            self.add_events(order.get_events())
            self.end_table()

        return "\n".join(self._text)

    def add_events(self, events):
        if events is None or len(events) == 0:
            self.add_info_line("No registered events yet.")
            return

        self.add_header()

        if self._last_event:
            self.add_event(events[-1])
            return

        for event in events:
            self.add_event(event)

    def add_header(self):
        self.begin_title_row()

        self.add_cell("Date/Time")
        self.add_cell("Status")

        if not self._short:
            self.add_cell("Description")
            self.add_cell("Position")

        self.end_row()

    def add_event(self, event):
        self.begin_row()

        self.add_cell(time.strftime(constants.LONG_DATE_FORMAT, event.get_date()))
        self.add_cell(event.get_text())
        if not self._short:
            self.add_cell(event.get_description())
            self.add_cell(event.get_location())

        self.end_row()

    def begin_table(self):
        self.add_line(TABLE_START_HTML)

    def end_table(self):
        self.add_line(TABLE_END_HTML)

    def begin_row(self):
        self.add_line(TABLE_ROW_HTML)

    def begin_title_row(self):
        self.add_line(TABLE_TITLE_ROW_HTML)

    def end_row(self):
        self.add_line(TABLE_END_ROW_HTML)

    def add_cell(self, cell_data):
        self.add_line(TABLE_CELL_HTML, cell_data)

    def add_info_line(self, data):
        self.add_line(INFO_LINE_HTML, data)

    def add_line(self, text, *args):
        self._text.append(text.format(*args).encode("utf-8"))


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
