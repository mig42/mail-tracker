# -*- coding: utf-8 *-*


class NotFoundOrder:
    def __init__(self, code):
        self._code = code

    def exists(self):
        return False

    def get_code(self):
        return self._code


class SentOrder:
    def __init__(self, code):
        self._code = code
        self._events = []

    def exists(self):
        return True

    def get_code(self):
        return self._code

    def add_event(self, event):
        self._events.append(event)

    def get_events(self):
        return self._events


