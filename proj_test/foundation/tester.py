# -*- coding: utf-8 -*-
import time

from cloud_testing.eptest_interface import CloudScheduler
from tools.device_helper import DeviceHelper
from tools.log_out import LogOut


class Tester(object):

    @classmethod
    def single_case_test(cls,
                         xcode_version,
                         driver_path,
                         test_log_path,
                         udid,
                         xctestrun_path,
                         ):
        """
        :param xcode_version: xcode version
        :param driver_path: driver_path
        :param test_log_path: test_log_path
        :param xctestrun_path: xctestrun_path
        :param udid: udid
        :return:
        """
        LogOut.log(" 📱 xcode_version：%s" % xcode_version)
        for i in range(30):
            if DeviceHelper.check_device(udid):
                LogOut.log(" 📱 设备已连接")
                break
            time.sleep(1)
        if not DeviceHelper.check_device(udid):
            return 1
        return_code = CloudScheduler.xcode_test(xcodebuild_version=xcode_version,
                                                xctestrun_path=xctestrun_path,
                                                log_path=test_log_path,
                                                derived_data_path=driver_path,
                                                skip_test_case=[])
        return return_code
