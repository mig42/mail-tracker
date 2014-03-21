# -*- coding: utf-8 *-*


class Event:
    def __init__(self, date, text, description, location):
        self.date = date
        self.text = text
        self.description = description
        self.location = location

    def get_date(self):
        return self.date

    def get_text(self):
        return self.text

    def get_description(self):
        return self.description

    def get_location(self):
        return self.location


class Location:
    def __init__(self, country="", city="", province=""):
        self.country = country
        self.city = city
        self.province = province

    def __str__(self):
        result = [self.country]
        if self.province != "":
            result.append(self.province)
        if self.city != "":
            result.append(self.city)

        result.reverse()

        return ", ".join(result)
