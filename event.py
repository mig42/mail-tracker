# -*- coding: utf-8 *-*


class Event:
    def __init__(self, date, text, description, location):
        self._date = date
        self._text = text
        self._description = description
        self._location = location

    def get_date(self):
        return self._date

    def get_text(self):
        return self._text

    def get_description(self):
        return self._description

    def get_location(self):
        return self._location


class Location:
    def __init__(self, country, city, province=""):
        self._country = country
        self._city = city
        self._province = province

    def __str__(self):
        result = []
        if self._country != "" and self._country is not None:
            result.append(self._country)
        if self._province != "" and self._province is not None:
            result.append(self._province)
        if self._city != "" and self._city is not None:
            result.append(self._city)

        result.reverse()

        return ", ".join(result)
