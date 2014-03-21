# -*- coding: utf-8 *-*


class NotFoundOrder:
    def __init__(self, code):
        self.code = code

    def exists(self):
        return False


class SentOrder:
    def __init__(self, code):
        self.code = code
        self.events = []

    def exists(self):
        return True

    def add_event(self, event):
        self.events.append(event)

    def get_events(self):
        return self.events


