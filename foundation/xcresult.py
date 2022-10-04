# -*- coding: utf-8 -*-

import re
import json
import subprocess
from tools.log_out import LogOut



class Xcresult:

    log_path = None

    def __init__(self, xcresult_path):
        self.result_path = xcresult_path
        self.parse_tool_path = "/Applications/Xcode.app/Contents/Developer/usr/bin/xcresulttool"

        self.tests_count = self.get_tests_count()  # case个数
        self.tests_failed_count = self.get_tests_failed_count()  # 失败case个数
        self.all_passed = True if self.get_tests_failed_count() == 0 else False  # 是否全部通过
        self.tests_passed_count = self.get_tests_passed_count()  # 通过case个数
        self.fail_case_result_array = self.parse_test_result()  # 所有失败case信息
        LogOut.log("📱用例数：%s 通过用例数：%s 失败用例数：%s" % (self.tests_count, self.tests_passed_count, self.tests_failed_count))
        LogOut.log("失败用例信息: %s" % (self.fail_case_result_array))

    def get_tests_count(self):
        """
        获取测试总次数
        """
        json_dic = self.get_json_result(self.result_path)
        metrics = json_dic["metrics"]

        LogOut.log(metrics)
        if "testsCount" not in metrics.keys():
            return 0
        return int(metrics["testsCount"]["_value"])

    def get_tests_failed_count(self):
        """
        获取测试失败次数
        """
        json_dic = self.get_json_result(self.result_path)
        metrics = json_dic["metrics"]
        count = 0
        if "testsFailedCount" in metrics.keys():
            count = int(metrics["testsFailedCount"]["_value"])
        return count

    def get_tests_passed_count(self):
        """
        获取测试通过的次数
        """
        pass_cases_count = int(self.get_tests_count()) - self.get_tests_failed_count()
        return pass_cases_count

    def parse_test_result(self):
        """
        获取所有失败case的信息
        """
        json_dic = self.get_json_result(self.result_path)
        issues = json_dic["issues"]
        if "testFailureSummaries" not in issues.keys():
            return []
        test_failure_summaries = issues["testFailureSummaries"]
        # 获取所有有问题的case的列表
        values_list = test_failure_summaries["_values"]
        case_result_arr = []
        for value in values_list:
            ret = Xcresult.fail_result_dic(value)
            case_result_arr.append(ret)
        return case_result_arr

    @classmethod
    def fail_result_dic(cls, dic):
        """
        生成失败case信息
        """
        message = dic["message"]["_value"]
        case_name = dic["testCaseName"]["_value"]
        reg = r'-(\[)(.*) (.*)(\])'
        match_obj = re.match(reg, case_name, re.M | re.I)
        class_name = None
        func_name = None
        if match_obj:
            class_name = match_obj.group(2)
            func_name = match_obj.group(3)
        else:
            print("未匹配")

        result_dic = {
            "class_name": class_name,
            "func_name": func_name,
            "failed_message": message,
            "pass": 0
        }
        return result_dic


    def get_json_result(self, result_path, ref_id=None):
        xcrun_tool_cmd = "xcrun " + self.parse_tool_path + " get --format json --path"
        cmd = "%s '%s'" % (xcrun_tool_cmd, self.result_path)
        if ref_id is not None:
            cmd = "%s '%s' --id '%s'" % (xcrun_tool_cmd, result_path, ref_id)
        result = subprocess.check_output(cmd, shell=True)
        return json.loads(result)
