# -*- coding: utf-8 -*-

"""
@author: ihenryhuang
@time: 2021/3/7 8:48 下午
@Copyright: Tencent. All rights reserved.

"""
from foundation.ui_operator.operate_path import Path
from foundation.foundation_path import PathHelper


class Cleaner(object):
    @classmethod
    def clean_derived_data(cls):
        derived_path = Path.driver_data_path()
        derived_test_path = Path.driver_data_path_for_test()
        PathHelper.clear(derived_path)
        PathHelper.clear(derived_test_path)


if __name__ == '__main__':
    Cleaner.clean_derived_data()
