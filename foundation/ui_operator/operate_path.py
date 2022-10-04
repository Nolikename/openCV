# -*- coding: utf-8 -*-
import os


class Path(object):

    @classmethod
    def plist_path(cls):
        moudle_dir = cls.__ui_operator_moudle_dir()
        return os.path.join(moudle_dir, "UIOperater/UIOperater/Info.plist")

    @classmethod
    def pbxproj_path(cls):
        moudle_dir = cls.__ui_operator_moudle_dir()
        return os.path.join(moudle_dir, "UIOperater/UIOperater.xcodeproj/project.pbxproj")

    @classmethod
    def proj_path(cls):
        moudle_dir = cls.__ui_operator_moudle_dir()
        return os.path.join(moudle_dir, "UIOperater/UIOperater.xcodeproj")

    @classmethod
    def __ui_operator_moudle_dir(cls):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return current_dir

    @classmethod
    def build_log_path(cls):
        moudle_dir = cls.__ui_operator_moudle_dir()
        return os.path.join(moudle_dir, "log/ui_build.log")
