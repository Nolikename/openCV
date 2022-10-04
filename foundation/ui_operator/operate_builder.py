# -*- coding: utf-8 -*-
import os
from foundation.ui_operator.operate_path import Path
from foundation.ui_operator.operate_cleaner import Cleaner


class Builder(object):

    @classmethod
    def clean_and_build(cls):
        cls.__clear_derived_data()
        cls.__xcode_clean()
        cls.__build()

    @classmethod
    def __clear_derived_data(cls):
        Cleaner.clean_derived_data()

    @classmethod
    def __xcode_clean(cls):
        xcodeproj_file_path = Path.proj_path()
        if os.path.exists(xcodeproj_file_path) is False:
            print(">>>>>>>>>>>>>  " + xcodeproj_file_path + "不存在")
            return False
        ret_code = os.system('xcodebuild clean -project ' + xcodeproj_file_path)
        return True if ret_code != 0 else False

    @classmethod
    def __build(cls):  # 如果要是没有build-derivedata的路径就新建
        build_log_path = Path.build_log_path()

        build_cmd = "/Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild build-for-testing -project "
        build_cmd += Path.proj_path()
        build_cmd += " -scheme UIOperaterUITests "
        build_cmd += "-derivedDataPath "
        build_cmd += Path.driver_data_path()
        build_cmd += " -sdk iphoneos"
        build_cmd += " > "
        build_cmd += build_log_path
        print(build_cmd)
        ret_code = os.system(build_cmd)
        if ret_code != 0:
            print(">>>>>>>>>>>>>  预处理工程编译失败，错误码 %s", ret_code)
            return False
        else:
            print(">>>>>>>>>>>>>  预处理工程编译成功")
            return True
        print("编译结束，查看编译日志%s" % (build_log_path))


if __name__ == '__main__':
    Builder.clean_and_build()
