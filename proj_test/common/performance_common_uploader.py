# -*- coding: utf-8 -*-
import os
from performance_test.proj_test.foundation.performance_foundation_api import EptestReporter
from tools.log_out import LogOut


class DataReporter(object):

    def __init__(self, debug=True):
        if debug:
            LogOut.log("测试环境")
        else:
            LogOut.log("正式环境")

        host = "https://openapi.tat.qq.com/"
        test_host = "https://test-openapi.tat.qq.com/"
        self.debug = debug
        self.host = test_host if debug is True else host

    # 上报性能数据
    def report_perf_data(self, params):
        LogOut.log("💻 上报性能数据")
        if params is None:
            return False
        interface = 'perf/SaveCompetitorPerf'
        return self.__post(interface, params)

    def start_record_calculate(self, params):
        LogOut.log("💻 调用录屏分帧服务")
        if params is None:
            return False
        interface = 'perf/StartCalculateRecordData'
        return self.__post(interface, params)

    # 上报case的执行结果
    def report_case_result(self, params):
        LogOut.log("💻 上报case执行结果")
        if params is None:
            LogOut.log("测试结果为空, 不上报测试结果")
            return True
        if self.debug:
            LogOut.log("测试环境, 不上报测试结果")
            return True
        interface = 'task/ReportCaseResult'
        return self.__post(interface, params)

    def __post(self, interface, params):
        url = self.host + interface
        LogOut.segment("🌍 发送网络请求")
        LogOut.log("请求链接 %s" % url)
        LogOut.log("请求参数 %s" % params)
        suc = EptestReporter().post(url=url, json_dict=params)
        if suc:
            LogOut.log("请求成功")
            return True
        else:
            LogOut.log("请求失败")
            return False

    def upload_file(self, log_path, triger_id, path=""):
        LogOut.log("💻 上传文件：%s" % log_path)
        """
        上报文件到cos
        """
        file_host = 'https://file.tat.qq.com/'
        if os.path.exists(log_path) is False:
            LogOut.log("需要上传的文件路径：%s 不存在" % log_path)
            return -1
        files = {"file": open(log_path, "rb")}
        if path:
            url = "{}log/upload?path={}&trgerId={}".format(file_host, path, triger_id)
        else:
            url = "{}log/upload?trigerId={}".format(file_host, triger_id)
        return EptestReporter().post_files(url, files)
