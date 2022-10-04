# -*- coding: utf-8 -*-

import os

from performance_test.foundation.foundation_path import PathHelper as FoundationPathHelper


class PerformancePathHelper(object):

    @classmethod
    def derived_data_path_for_test(cls, udid, flag=""):
        # test的driver_data
        return os.path.join(cls.tmp_folder_path(udid), "DerivedData/" + str(flag))

    @classmethod
    def tmp_folder_path(cls, udid):
        # tmp文件夹
        return os.path.join(os.path.join(cls.script_folder_path(), "tmp"), udid)

    @classmethod
    def script_folder_path(cls):
        # Python脚本所在的目录
        return os.path.join(FoundationPathHelper.project_path(), "proj_test")

    @classmethod
    def mount_point_path(cls, udid):
        return os.path.join(cls.tmp_folder_path(udid), "point")

    @classmethod
    def log_dir(cls):
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_dir = os.path.join(path, "log")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return log_dir

    @classmethod
    def log_path(cls, identifier):
        return os.path.join(cls.log_dir(), identifier)

    @classmethod
    def derived_path(cls, udid, bundle_id, path):
        derived_path = os.path.join(path, udid, bundle_id)
        if not os.path.exists(derived_path):
            os.makedirs(derived_path)
        return derived_path

