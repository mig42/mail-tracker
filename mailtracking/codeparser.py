# -*- coding: utf-8 *-*

CODE_SEPARATOR = "#"


class CodeParser:
    def __init__(self, lines):
        self._lines = lines
        self._codes = []
        self.parse()

    def parse(self):
        for line in self._lines:
            split_line = line.split(CODE_SEPARATOR)
            if len(split_line) < 2:
                self._codes.append(Code(split_line[0]))
                continue
            self._codes.append(Code(split_line[0], split_line[1]))

    def get_codes(self):
        return self._codes


class Code:
    def __init__(self, code, identifier=None):
        self._code = code.strip()
        self._identifier = identifier.strip()

    def get_code(self):
        return self._code

    def get_identifier(self):
        if self._identifier is None or self._identifier == "":
            return self._code
        return self._identifier
