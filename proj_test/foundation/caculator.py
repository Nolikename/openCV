# -*- coding: utf-8 -*-

class Calculator(object):

    @classmethod
    def max(cls, value_string):
        str_list = value_string.split(",")
        return max(str_list)

    @classmethod
    def min(cls, value_string):
        str_list = value_string.split(",")
        return min(str_list)

    @classmethod
    def avg(cls, value_string):
        if not value_string:
            return 0
        str_list = value_string.split(",")
        total = 0
        for num_str in str_list:
            total += float(num_str)
        avg = float(total) / float(len(str_list))
        return str(avg)
