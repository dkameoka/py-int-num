#!/usr/bin/env python3

import itertools
from dataclasses import dataclass


@dataclass
class _EnglishCardinal:
    units: str
    teens: str
    tens: str


@dataclass
class _LatinCardinal:
    prefix: str
    units: str
    tens: str
    hundreds: str


class IntegerToEnglishLatin:

    ENG_TABLE = {
        0: _EnglishCardinal('',      'ten',       ''),
        1: _EnglishCardinal('one',   'eleven',    ''),
        2: _EnglishCardinal('two',   'twelve',    'twenty'),
        3: _EnglishCardinal('three', 'thirteen',  'thirty'),
        4: _EnglishCardinal('four',  'fourteen',  'forty'),
        5: _EnglishCardinal('five',  'fifteen',   'fifty'),
        6: _EnglishCardinal('six',   'sixteen',   'sixty'),
        7: _EnglishCardinal('seven', 'seventeen', 'seventy'),
        8: _EnglishCardinal('eight', 'eighteen',  'eighty'),
        9: _EnglishCardinal('nine',  'nineteen',  'ninety')}

    LAT_TABLE = {
        0: _LatinCardinal('n',     '',         '',             ''),
        1: _LatinCardinal('m',     'un',       'deci',         'centi'),
        2: _LatinCardinal('b',     'duo',      'viginti',      'ducenti'),
        3: _LatinCardinal('tr',    'tre',      'triginta',     'trecenti'),
        4: _LatinCardinal('quadr', 'quattuor', 'quadraginta',  'quadringenti'),
        5: _LatinCardinal('quint', 'quin',     'quinquaginta', 'quingenti'),
        6: _LatinCardinal('sext',  'sex',      'sexaginta',    'sescenti'),
        7: _LatinCardinal('sept',  'septen',   'septuaginta',  'septingenti'),
        8: _LatinCardinal('oct',   'octo',     'octoginta',    'octingenti'),
        9: _LatinCardinal('non',   'novem',    'nonaginta',    'nongenti')}

    def __init__(self, number):
        self.number = int(number)

    def _triplets(self, number_str):
        num_iter = iter(map(int, reversed(str(number_str))))
        return itertools.zip_longest(num_iter, num_iter, num_iter, fillvalue=0)

    def _english_cardinal_numeral(self, units, tens, hundreds):
        result = []
        if hundreds > 0:
            result.append(self.ENG_TABLE[hundreds].units + ' hundred')
        if tens > 0:
            if tens == 1:
                result.append(self.ENG_TABLE[units].teens)
            elif units > 0:
                result.append(
                    self.ENG_TABLE[tens].tens + '-' + self.ENG_TABLE[units].units)
            else:
                result.append(self.ENG_TABLE[tens].tens)
        else:
            result.append(self.ENG_TABLE[units].units)
        return ' '.join(filter(len, result))

    def _latin_from_short_scale(self, exp_short_scale):
        if exp_short_scale < 1:
            return 'thousand'
        result = []
        for units, tens, hundreds in self._triplets(exp_short_scale):
            if hundreds == 0 and tens == 0:
                result.insert(0, self.LAT_TABLE[units].prefix + 'illi')
                continue
            if hundreds == 1 and tens == 0 and units == 3:  # Special case for 103
                result.insert(0, 'trescentilli')
                continue
            part = self.LAT_TABLE[units].units + \
                self.LAT_TABLE[tens].tens + self.LAT_TABLE[hundreds].hundreds
            if part[-1] in ['a', 'e', 'o']:  # Replace some endings
                part = part[:-1] + 'i'
            part += 'lli'
            result.insert(0, part)
        return ''.join(filter(len, result)) + 'on'

    def __str__(self):
        if self.number == 0:
            return 'zero'
        result = []
        negative = ''
        if self.number < 0:
            self.number = -self.number
            negative = 'negative '
        for triplet_index, (units, tens, hundreds) in enumerate(self._triplets(self.number)):
            numeral = self._english_cardinal_numeral(units, tens, hundreds)
            if len(numeral) == 0:
                continue
            if triplet_index < 1:
                result.append(numeral)
                continue
            short_numeric_scale = triplet_index - 1
            result.insert(0, numeral + ' ' +
                          self._latin_from_short_scale(short_numeric_scale))
        return negative + ' '.join(result)
