# -*- coding: utf-8 -*-

"""
@author: ihenryhuang
@time: 2021/3/22 8:38 下午
@Copyright: Tencent. All rights reserved.

"""
import json
import os
import time
import subprocess

import ios_setting
from attaapi.atta_api import AttaRequest
from cloud_testing import device
from cloud_testing.eptest_interface import CloudScheduler
from performance_test.foundation.foundation_path import PathHelper
from performance_test.foundation.shell import Shell
from performance_test.foundation.video import INIT, stop_record, start_record
from performance_test.proj_test.common.data_processor import DataProcessor
from performance_test.proj_test.common.path import PerformancePathHelper
from performance_test.proj_test.foundation.tester import Tester
from tools import xctestrun_helper, report, command
from tools.device_helper import DeviceHelper
from tools.except_helper import UnexpectedError, ExceptionField
from tools.log_out import LogOut
from performance_test.foundation.installer import Installer
from tools.robot_helper import RobotHelper

PRODUCT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_TXT_PATH = "output/test.txt"
DEBUG_IPHONEOS_PATH = "output/Build/Products"
DEBUG_IPHONEOS_PATH11 = "output/Build/Products11"
DEBUG_IPHONEOS_PATH12 = "output/Build/Products12"
DEBUG_IPHONEOS_PATH13 = "output/Build/Products13"
DEBUG_IPHONEOS = "Debug-iphoneos"
XCODE_VERSION = "max"

UI_OPERATER = "UIOperater.app"
UI_OPERATER_BUNDLE_ID = "com.tencent.perf.automation"
UITEST_OPERATER = "UIOperaterUITests-Runner.app"
UITEST_OPERATER_BUNDLE_ID = "com.tencent.perf.automation.xctrunner"

UITEST = "UIOperaterUITests"
TEST_BUNDLE = "testAppBundleId"
ITERATION = "iteration"


def wetest_suitable_test(udid):
    """
    获取云测合适的版本去执行, 由于云测存在iOS13和14两种arm64e的机型且打出来的二进制包又不兼容，故需要兼容处理
    :param udid: 设备udid
    """
    global XCODE_VERSION
    global DEBUG_IPHONEOS_PATH
    XCODE_VERSION = "max"
    if DeviceHelper.is_below_ios_14(udid):
        XCODE_VERSION = "11.6"

    if XCODE_VERSION == "max" and os.path.exists(os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH13)):
        LogOut.log(" path {}".format(os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH13)))
        DEBUG_IPHONEOS_PATH = DEBUG_IPHONEOS_PATH13
    if XCODE_VERSION == "12.3" and os.path.exists(os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH12)):
        LogOut.log(" path {}".format(os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH12)))
        DEBUG_IPHONEOS_PATH = DEBUG_IPHONEOS_PATH12
    if XCODE_VERSION == "11.6" and os.path.exists(os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH11)):
        LogOut.log(" path {}".format(os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH11)))
        DEBUG_IPHONEOS_PATH = DEBUG_IPHONEOS_PATH11
    LogOut.log("DEBUG_IPHONEOS_PATH {}".format(DEBUG_IPHONEOS_PATH))


def install_alert_app(udid):
    DeviceHelper.uninstall_app(udid, UITEST_OPERATER_BUNDLE_ID)
    DeviceHelper.uninstall_app(udid, UI_OPERATER_BUNDLE_ID)
    RUNNER_PATH = os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH, DEBUG_IPHONEOS, UITEST_OPERATER)
    APP_PATH = os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH, DEBUG_IPHONEOS, UI_OPERATER)
    CloudScheduler.synchronize_resource_to_mac(xctestrun_path=get_xctestrun_path(),
                                               cation_tag=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                       DEBUG_IPHONEOS_PATH),
                                               only_update_testrun=False,
                                               should_resign=True)
    install_test_app(udid, UITEST_OPERATER_BUNDLE_ID, RUNNER_PATH)
    install_test_app(udid, UI_OPERATER_BUNDLE_ID, APP_PATH)

    # upload_file(udid)


def get_xctestrun_path():
    xctestrun_path = PathHelper.match_wildcard(os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH), "*.xctestrun")
    if len(xctestrun_path) <= 0:
        return None
    return xctestrun_path[0]


def init_performance(bundle_id, udid, launch_cases, save_path):
    """
    :param save_path: 保存视频结果的文件夹
    :param bundle_id: bundleid
    :param udid: udid
    :param launch_cases: ["Launch/testFirstLaunch", "Launch/testFirstLaunch2"]
    :return:
    """
    LogOut.log("init_performance bundle_id {}; launch_cases {}".format(bundle_id, launch_cases))
    if len(launch_cases) <= 0:
        return
    derived_path = PerformancePathHelper.derived_data_path_for_test(udid, "init_performance_{}".format(time.time()))
    test_log_path = os.path.join(save_path, "init_performance_{}".format(time.time()) + ".log")
    start_record()
    xctestrun_path = modify_testing_environment(launch_cases, TEST_BUNDLE, bundle_id)
    return_code = Tester.single_case_test(XCODE_VERSION, derived_path, test_log_path, udid, xctestrun_path)
    stop_record(save_path, bundle_id, udid, type=INIT)
    LogOut.log(" 📱 init_performance：%s" % return_code)


def modify_testing_environment(test_plan, env_name="", env_value=""):
    xctestrun_path = get_xctestrun_path()

    if env_name != "":
        target_env_variables = xctestrun_helper.testing_environment_variables(xctestrun_path)
        daemon_env_variables = target_env_variables.get(UITEST, {})
        daemon_env_variables[env_name] = env_value
        xctestrun_helper.modify_testing_environment_variables(xctestrun_path, daemon_env_variables)
    xctestrun_helper.add_xctestrun_testcase(xctestrun_path, test_plan)
    return xctestrun_path


def get_config():
    config_path = get_config_path()
    with open(config_path) as config_file:
        config = json.load(config_file)
        LogOut.log("config {}".format(config))
    config_file.close()
    return config


def get_config_path():
    LogOut.log("DEBUG_IPHONEOS_PATH {}".format(DEBUG_IPHONEOS_PATH))
    config_path = os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH, "config.json")
    if not os.path.exists(config_path):
        LogOut.error("config not exists: {}".format(config_path))
        return None
    return config_path


def install_test_app(udid, bundle_id, app_path, failed_warning=True):
    """
    手机没有app才手动安装，其余情况测试的时候覆盖安装

    :param :bundle_id app包BundleId
    :param :failed_warning 失败发送警告
    :return bool 是否安装成功
    """
    LogOut.log("【安装】目标app包:{}".format(app_path))
    if not app_path:
        LogOut.log("【安装】目标app包{}不存在".format(bundle_id))
        return False

    LogOut.log("【安装】使用ideviceinstaller安装目标App:{}".format(bundle_id))
    if app_path.endswith(".ipa"):
        LogOut.log("【安装】使用ideviceinstaller安装目标App:{}".format(bundle_id))
        is_success = Installer.check_install(udid, bundle_id, app_path)
    elif ios_setting.SINGLETON.run_on_cloud:
        LogOut.log("【安装】使用云测接口方法安装目标App:{}".format(bundle_id))
        is_success = CloudScheduler.install_app(app_path)
    else:
        LogOut.log("【安装】使用ideviceinstaller安装目标App:{}".format(bundle_id))
        is_success = Installer.check_install(udid, bundle_id, app_path)

    if is_success:
        return is_success

    if not failed_warning:
        return

    send_info = "【安装】{}App尝试安装到{}失败".format(bundle_id, udid)
    LogOut.log(send_info)
    LogOut.log("【安装】安装目标App到{}失败，如果后续测试可能是重签问题请先保证原始构建包可以安装，"
               "否则请联系设备管理的同事！！！".format(udid))
    AttaRequest.send_error_info(UnexpectedError.PRE_INSTALL_FAILED.value[ExceptionField.CODE],
                                "【安装】安装{}失败，换机重试".format(bundle_id))
    RobotHelper(ios_setting.SINGLETON.robot_info).report_robot_simple_info(send_info)
    RobotHelper(ios_setting.SINGLETON.robot_info).report_utest_message(send_info)
    return is_success


def upload_file(udid):
    try:
        upload_path = os.path.join(PRODUCT_DIR, DEBUG_IPHONEOS_PATH, "marked/upload/")
        upload_dirs = os.listdir(upload_path)
        for upload_dir in upload_dirs:
            DataProcessor.add_dir_to_sandbox(udid, upload_dir, os.path.join(upload_path, upload_dir))
    except Exception as e:
        LogOut.log("e {}".format(e))
