#!/usr/bin/env python3

import itertools

class IntegerToEnglishLatin:
    def __init__(self,number):
        assert isinstance(number,int)
        self.number = number

    def _triplets(self,number_str):
        num_iter = iter(map(int,reversed(str(number_str))))
        return itertools.zip_longest(num_iter,num_iter,num_iter,fillvalue = 0)

    def _english_cardinal_numeral(self,units,tens,hundreds):
        cardinal_table = {
            0:['','ten',''],
            1:['one','eleven',''],
            2:['two','twelve','twenty'],
            3:['three','thirteen','thirty'],
            4:['four','fourteen','forty'],
            5:['five','fifteen','fifty'],
            6:['six','sixteen','sixty'],
            7:['seven','seventeen','seventy'],
            8:['eight','eighteen','eighty'],
            9:['nine','nineteen','ninety']}
        result = []
        if hundreds > 0:
            result.append(cardinal_table[hundreds][0] + ' hundred')
        if tens > 0:
            if tens == 1:
                result.append(cardinal_table[units][1])
            elif units > 0:
                result.append(cardinal_table[tens][2] + '-' + cardinal_table[units][0])
            else:
                result.append(cardinal_table[tens][2])
        else:
            result.append(cardinal_table[units][0])
        return ' '.join(filter(len,result))

    def _latin_from_short_scale(self,exp_short_scale):
        cg_table = {
            0:['n','','',''],
            1:['m','un','deci','centi'],
            2:['b','duo','viginti','ducenti'],
            3:['tr','tre','triginta','trecenti'],
            4:['quadr','quattuor','quadraginta','quadringenti'],
            5:['quint','quin','quinquaginta','quingenti'],
            6:['sext','sex','sexaginta','sescenti'],
            7:['sept','septen','septuaginta','septingenti'],
            8:['oct','octo','octoginta','octingenti'],
            9:['non','novem','nonaginta','nongenti']}
        if exp_short_scale < 1:
            return 'thousand'
        result = []
        for units,tens,hundreds in self._triplets(exp_short_scale):
            if hundreds == 0 and tens == 0:
                result.insert(0,cg_table[units][0] + 'illi')
                continue
            if hundreds == 1 and tens == 0 and units == 3: #Special case for 103
                result.insert(0,'trescentilli')
                continue
            part = cg_table[units][1] + cg_table[tens][2] + cg_table[hundreds][3]
            if part[-1] in ['a','e','o']: # Replace some endings
                part = part[:-1] + 'i'
            part += 'lli'
            result.insert(0,part)
        return ''.join(filter(len,result)) + 'on'

    def __str__(self):
        if self.number == 0:
            return 'zero'
        result = []
        negative = ''
        if self.number < 0:
            self.number = -self.number
            negative = 'negative '
        for triplet_index,(units,tens,hundreds) in enumerate(self._triplets(self.number)):
            numeral = self._english_cardinal_numeral(units,tens,hundreds)
            if len(numeral) == 0:
                continue
            if triplet_index < 1:
                result.append(numeral)
                continue
            short_numeric_scale = triplet_index - 1
            result.insert(0,numeral + ' ' + self._latin_from_short_scale(short_numeric_scale))
        return negative + ' '.join(result)
