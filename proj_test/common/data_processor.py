# -*- coding: utf-8 -*-
import json
import os
import shutil
import time

from performance_test.foundation.perfdog.perfdog import PerfDog
from performance_test.proj_test.common.path import PerformancePathHelper
from tools.device_helper import DeviceHelper
from tools.log_out import LogOut

UITEST_OPERATER_BUNDLE_ID = "com.tencent.perf.automation.xctrunner"


class DataProcessor(object):

    @classmethod
    def process_data(cls, values, udid, bundle_id):
        try:
            mount_root_dir = PerformancePathHelper.mount_point_path(udid)
            code = DeviceHelper.mount(udid, bundle_id, mount_root_dir)
            if code != 0:
                LogOut.log("【拷贝pflog】挂载App沙盒失败{}".format(mount_root_dir))
                return
            app_log_path = cls.performance_log_path(mount_root_dir)
            PerfDog.write_values_to_log(app_log_path, values)
            DeviceHelper.umount(mount_root_dir)
        except ValueError as err:
            LogOut.log("【拷贝pflog】从App沙盒获取pflog失败: {}".format(err))

    @classmethod
    def performance_log_path(cls, mount_root_dir):
        LogOut.log("performance_log_path")
        LogOut.log(os.listdir(mount_root_dir))
        LogOut.log(os.listdir(os.path.join(mount_root_dir, "Documents")))
        LogOut.log(os.listdir(os.path.join(mount_root_dir, "Documents/NPTTrail")))
        LogOut.log(os.listdir(os.path.join(mount_root_dir, "Documents/NPTTrail/tmp")))
        LogOut.log("performance_log_path end")

        app_log_path = os.path.join(mount_root_dir, "Documents/NPTTrail/tmp/")
        if not os.path.exists(app_log_path):
            LogOut.log("【拷贝pflog】App沙盒中不存在NTLog:{}".format(app_log_path))
            DeviceHelper.umount(mount_root_dir)
            return None
        for root, _, files in os.walk(app_log_path):
            pflog_file = None
            for file in files:
                pflog_file = os.path.join(root, file)

        return pflog_file

    @classmethod
    def add_dir_to_sandbox(cls, udid, bundle_id, upload_dir):
        mount_root_dir = PerformancePathHelper.mount_point_path(udid)
        try:
            code = DeviceHelper.mount(udid, bundle_id, mount_root_dir)
            if code != 0:
                LogOut.log("【add_dir_to_sandbox】挂载App沙盒失败{}".format(mount_root_dir))
                return None
            target_dir = os.path.join(mount_root_dir, "Documents")
            shutil.move(upload_dir, target_dir)
        except ValueError as err:
            LogOut.log("【拷贝pflog】从App沙盒获取pflog失败: {}".format(err))
            return None
        except Exception as err:
            LogOut.log("【拷贝pflog】从App沙盒获取pflog失败: {}".format(err))
            return None
        finally:
            DeviceHelper.umount(mount_root_dir)


    @classmethod
    def get_perf_log_file(cls, udid, result_path):
        try:
            mount_root_dir = PerformancePathHelper.mount_point_path(udid)
            code = DeviceHelper.mount(udid, UITEST_OPERATER_BUNDLE_ID, mount_root_dir)
            if code != 0:
                LogOut.log("【拷贝pflog】挂载App沙盒失败{}".format(mount_root_dir))
                return None
            app_log_path = cls.performance_log_path(mount_root_dir)
            with open(app_log_path) as log_file:
                log_data = json.load(log_file)
            LogOut.log("【拷贝pflog] log_data {}".format(log_data))
            result_dir = os.path.join(result_path, UITEST_OPERATER_BUNDLE_ID)
            if not os.path.exists(result_dir):
                os.makedirs(result_dir)
            save_file = os.path.join(result_dir, "{}.json".format(int(time.time())))
            with open(save_file, "w") as result_file:
                json.dump(log_data, result_file)
            DeviceHelper.umount(mount_root_dir)
            LogOut.log("【拷贝pflog] save_file {}".format(save_file))
            return save_file
        except ValueError as err:
            LogOut.log("【拷贝pflog】从App沙盒获取pflog失败: {}".format(err))
            return None
        except Exception as err:
            LogOut.log("【拷贝pflog】从App沙盒获取pflog失败: {}".format(err))
            return None
