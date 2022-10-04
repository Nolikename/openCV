# -*- coding: utf-8 -*-

"""
@author: ihenryhuang
@time: 2021/3/10 3:49 下午
@Copyright: Tencent. All rights reserved.

"""
import os
import shutil
from tools.log_out import LogOut
from performance_test.proj_test.common.path import PerformancePathHelper
from tools.device_helper import DeviceHelper


NTLOG_DIR_NAME = "ntlog"
NTLOG_DIR = "Library/NTLog"

PERF_DIR_NAME = "pflog"
PERF_DIR = "Documents/NPTTrail/tmp/"


def copy_app_pflog(app_bundle_id, device_udid, destination_path):
    try:
        mount_root_dir = PerformancePathHelper.mount_point_path(device_udid)
        mac_performance_path = os.path.join(destination_path, PERF_DIR_NAME, app_bundle_id)
        code = DeviceHelper.mount(device_udid, app_bundle_id, mount_root_dir)
        if code != 0:
            LogOut.log("【拷贝pflog】挂载App沙盒失败{}".format(mount_root_dir))
            return

        app_log_path = os.path.join(mount_root_dir, PERF_DIR)
        if not os.path.exists(app_log_path):
            LogOut.log("【拷贝pflog】App沙盒中不存在NTLog:{}".format(app_log_path))
            DeviceHelper.umount(mount_root_dir)
            return

        if not os.path.exists(destination_path):
            LogOut.log("【拷贝pflog】在Mac上创建NTLog存放路径:{}".format(destination_path))
            os.makedirs(destination_path)

        shutil.rmtree(mac_performance_path, True)
        shutil.copytree(app_log_path, mac_performance_path)
    except ValueError as err:
        LogOut.log("【拷贝pflog】从App沙盒获取pflog失败: {}".format(err))
    DeviceHelper.umount(mount_root_dir)


def copy_app_ntlog(app_bundle_id, device_udid, destination_path):
    """
    把App沙盒中的NTLog拷贝到本地test_result/NTLog路径下

    app_bundle_id: app bundle id
    device_udid: 目标设备
    mount_root_dir: 沙盒挂载点
    to_dest_path: 目标路径
    """
    try:
        mount_root_dir = PerformancePathHelper.mount_point_path(device_udid)
        mac_ntlog_path = os.path.join(destination_path, NTLOG_DIR_NAME)
        code = DeviceHelper.mount(device_udid, app_bundle_id, mount_root_dir)
        if code != 0:
            LogOut.log("【拷贝NTLog】挂载App沙盒失败{}".format(mount_root_dir))
            return

        app_log_path = os.path.join(mount_root_dir, NTLOG_DIR)
        if not os.path.exists(app_log_path):
            LogOut.log("【拷贝NTLog】App沙盒中不存在NTLog:{}".format(app_log_path))
            DeviceHelper.umount(mount_root_dir)
            return

        create_dir_if_needed(destination_path)

        shutil.rmtree(mac_ntlog_path, True)
        shutil.copytree(app_log_path, mac_ntlog_path)
    except ValueError as err:
        LogOut.log("【拷贝NTLog】从App沙盒获取NTLog失败: {}".format(err))
    finally:
        DeviceHelper.umount(mount_root_dir)


def create_dir_if_needed(destination_path):
    if not os.path.exists(destination_path):
        LogOut.log("【拷贝NTLog】在Mac上创建NTLog存放路径:{}".format(destination_path))
        os.makedirs(destination_path)
