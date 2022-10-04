# -*- coding: utf-8 -*-

"""
@author: ihenryhuang
@time: 2021/3/11 10:25 上午
@Copyright: Tencent. All rights reserved.

"""
import os
import json

from cloud_testing.eptest_interface import CloudScheduler

from performance_test.foundation.foundation_path import PathHelper
from performance_test.foundation.sql import Performance_Sql
from performance_test.proj_test.common import ntlog
from performance_test.proj_test.common.data_processor import DataProcessor
from performance_test.proj_test.common.path import PerformancePathHelper
from performance_test.foundation.xcresult import Xcresult
from tools.log_out import LogOut


class TestResult(object):

    @classmethod
    def performance_result(cls, triger_id, derived_path, udid):
        test_results_dir = os.path.join(derived_path, "Logs/Test")
        pflog_path = None
        pflog_dir_path = os.path.join(test_results_dir, "pflog")

        paths_arr = PathHelper.find_all_files(pflog_dir_path)
        if paths_arr:
            pflog_path = paths_arr[0]
        data = None
        if pflog_path is None:
            LogOut.log("没有找到性能测试数据")
            return None
        with open(pflog_path) as file:
            data = json.load(file)
            data["TaskId"] = str(triger_id)
            data["DeviceId"] = udid
            file.close()
        final_data = {
            "CompetitorPerfInfo": data
        }
        return final_data

    @classmethod
    def save_performance_result(cls, udid, bundle_id, app_name, test_time, result_path):
        pflog_path = DataProcessor.get_perf_log_file(udid, result_path)
        if pflog_path is None:
            LogOut.log("没有找到性能测试数据")
            return None
        with open(pflog_path) as file:
            data = json.load(file)
            file.close()
        Performance_Sql.insert_task(**{
            "device_id": udid,
            "bundle_id": bundle_id,
            "product_name": data["ProductName"],
            "app_name": app_name,
            "os": data["OS"],
            "os_ver": data["OSVer"],
            "app_version": data["AppVersion"],
            "device_name": data["DeviceName"],
            "app_build_num": data["AppBuildNum"],
        })
        for detail in data["Detail"]:
            for result in detail["Result"]:
                Performance_Sql.insert_case(**{
                    "test_time": test_time,
                    "device_id": udid,
                    "bundle_id": bundle_id,
                    "case_name": detail["CaseName"],
                    "index_name": result["Name"],
                    "app_name": app_name,
                    "value": result["Value"],
                    "threshold": result["Threshold"],
                    "threshold_up": result["ThresholdUp"],
                    "threshold_down": result["ThresholdDown"],
                    "comparison_mode": result["ComparisonMode"],
                    "unit": result["Unit"],
                    "computing_percent": result["ComputingPercent"],
                })

    @classmethod
    def save_opencv_result(cls, udid, bundle_id, app_name, test_time, result_path, values):
        pflog_path = DataProcessor.get_perf_log_file(udid, result_path)
        if pflog_path is None:
            LogOut.log("没有找到性能测试数据")
            return None
        with open(pflog_path) as file:
            data = json.load(file)
            file.close()
        Performance_Sql.insert_task(**{
            "device_id": udid,
            "bundle_id": bundle_id,
            "product_name": data["ProductName"],
            "app_name": app_name,
            "os": data["OS"],
            "os_ver": data["OSVer"],
            "app_version": data["AppVersion"],
            "device_name": data["DeviceName"],
            "app_build_num": data["AppBuildNum"],
        })
        for detail in data["Detail"]:
            for result in detail["Result"]:
                Performance_Sql.insert_case(**{
                    "test_time": test_time,
                    "device_id": udid,
                    "bundle_id": bundle_id,
                    "case_name": detail["CaseName"],
                    "index_name": result["Name"],
                    "app_name": app_name,
                    "value": ','.join(str(value) for value in values),
                    "threshold": result["Threshold"],
                    "threshold_up": result["ThresholdUp"],
                    "threshold_down": result["ThresholdDown"],
                    "comparison_mode": result["ComparisonMode"],
                    "unit": result["Unit"],
                    "computing_percent": result["ComputingPercent"],
                })

    @classmethod
    def test_result(cls, triger_id, ret_code, casename, udid, product_name):
        # xcresult_path = TestResult.xcresult_path(udid, casename)
        # if not xcresult_path:
        #     return None
        # LogOut.log("xcresult_path {}".format(xcresult_path))
        return TestResult.result_from_xcresult(triger_id, ret_code, casename, udid, "xcresult_path", product_name)

    @classmethod
    def result_from_xcresult(cls, triger_id, ret_code, casename, udid, xcresult_path, product_name, env=False):
        # result = Xcresult(xcresult_path)
        # single_result = None
        # passed = result.all_passed

        single_result = {
            "class_name": casename.split('/')[0],
            "func_name": casename.split('/')[1],
            "failed_message": "",
            "pass": 1 if ret_code == 0 else 0
        }
        # if ret_code == 0:
        # # if passed:
        #     single_result = {
        #         "class_name": casename.split('/')[0],
        #         "func_name": casename.split('/')[1],
        #         "failed_message": "",
        #         "pass": 1
        #     }
        # else:
        #     if result.fail_case_result_array:
        #         single_result = result.fail_case_result_array[0]
        #     if single_result is None:
        #         return None

        reportUrl = "http://testone.woa.com/eptest.compare-chart?" \
                    "task_id={}&product_name={}".format(triger_id, product_name)
        if env:
            reportUrl = "http://test.testone.woa.com/eptest.compare-chart?" \
                        "task_id={}&product_name={}".format(triger_id, product_name)
        result_dic = {
            "debugCommand": "",
            "stackTrace": "",
            "methodName": single_result["func_name"],
            "execTime": 0,
            "caseResult": single_result["pass"],
            "className": single_result["class_name"],
            "deviceId": udid,
            "reportUrl": reportUrl
        }

        # if passed is False:
        #     result_dic["FailedCode"] = ret_code
        #     result_dic["FailedReason"] = single_result["failed_message"]

        result_dic_arr = []
        result_dic_arr.append(result_dic)

        case_result_dic = {
            "trigerId": triger_id,
            "caseList": result_dic_arr,
        }

        return case_result_dic

    @classmethod
    def xcresult_path(cls, udid, case_name):
        derived_path = PerformancePathHelper.derived_data_path_for_test(udid, case_name)
        test_results_dir = os.path.join(derived_path, "Logs/Test")
        paths = PathHelper.match_wildcard(test_results_dir, "*.xcresult")
        if paths is None or len(paths) is 0:
            return None
        LogOut.log("files Logs/Test {}".format(os.listdir(test_results_dir)))
        xcresult_path = PathHelper.match_wildcard(test_results_dir, "*.xcresult")[0]
        return xcresult_path
