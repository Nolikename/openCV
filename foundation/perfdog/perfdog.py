# -*- coding: utf-8 -*-
import subprocess
import time
import traceback
import shutil
import os
import json

import numpy as np

from performance_test.foundation.file import download_file, untar
from performance_test.foundation.perfdog import perfdog_pb2_grpc
from performance_test.foundation.perfdog import perfdog_pb2
import grpc
import shlex

from performance_test.foundation.perfdog.perfdog_const import PERFDOG_SERVICE_DIR, PLATFORM_CONF, current_dir
from performance_test.foundation.sql import Performance_Sql
from performance_test.proj_test.foundation.caculator import Calculator
from tools.log_out import LogOut

# ihenryhuang的token 20台多点登录权限
TOKEN = '756be8ca6fe246f1b2343a414256d3f3393aa3cb3b7faad1ec04449a0c40bfbb'
PERFDOG_PATH_UTEST = "/Users/utest/utest_data/tools/PerfDogService/PerfDogService"
PERFDOG_PATH_LOCAL = "/Users/henry/PerfDogService/PerfDogService"


class PerfDog(object):
    def __init__(self, output_dir):
        self.result_file_path = None
        self.perf_dog_start_time = None
        self.perfdog_output = None
        self.__set_output_dir(output_dir)
        self.__clear_output()

        if os.path.exists(PERFDOG_PATH_UTEST):
            subprocess.Popen(PERFDOG_PATH_UTEST)
        else:
            self.__download_pd()
            # 填入PerfDogService的路径
            subprocess.Popen(os.path.join(PERFDOG_SERVICE_DIR, PLATFORM_CONF["executable_file_name"]))
        time.sleep(5)
        LogOut.log("PerfDog创建stub")
        stub = self.__create_stub()
        self.stub = stub
        LogOut.log("PerfDog账号登录")
        self.__login(stub)

    @staticmethod
    def __download_pd():
        """
        初次使用下载PerfDogService, 检查如果有的话就不下载了
        """
        if os.path.exists(PERFDOG_SERVICE_DIR):
            return
        LogOut.log("下载PerfDogService")
        try:
            download_name = os.path.join(current_dir, PLATFORM_CONF["download_name"])
            download_file(PLATFORM_CONF["url"], download_name)
            untar(download_name, PERFDOG_SERVICE_DIR)
            os.remove(download_name)
        except IOError as e:
            LogOut.error(str(e))

    def __set_output_dir(self, path):
        self.perfdog_output = os.path.join(path, "perfdog_output")
        LogOut.log("self.perfdog_output {}".format(self.perfdog_output))

    def __output_dir(self):
        LogOut.log("__output_dir perfdog_output {}".format(self.perfdog_output))
        return self.perfdog_output

    def __clear_output(self):
        path = self.__output_dir()
        if os.path.exists(path):  # 如果文件存在
            # 删除文件，可使用以下两种方法。
            shutil.rmtree(path)
        os.makedirs(path)

    def __create_stub(self):
        options = [('grpc.max_receive_message_length', 100 * 1024 * 1024)]
        channel = grpc.insecure_channel('127.0.0.1:23456', options=options)
        stub = perfdog_pb2_grpc.PerfDogServiceStub(channel)
        return stub

    def __login(self, stub):
        userInfo = stub.loginWithToken(perfdog_pb2.Token(token=TOKEN))
        LogOut.log("\nPerfDog登录信息")
        print(userInfo)

    def start_monitor(self, udid, bundle_id):
        self.perf_dog_start_time = int(round(time.time() * 1000))
        try:
            stub = self.stub
            deviceEventIterator = stub.startDeviceMonitor(perfdog_pb2.Empty())
            for deviceEvent in deviceEventIterator:
                # 从DeviceEvent中获取到device对象，device对象会在后面的接口中用到
                device = deviceEvent.device
                self.device = device
                if deviceEvent.eventType == perfdog_pb2.ADD:
                    # 每台手机会返回两个conType不同的设备对象(USB的和WIFI的),如果是测有线，取其中的USB对象
                    if device.conType == perfdog_pb2.USB and device.uid == udid:
                        LogOut.log("PerfDog找到目标设备并初始化设备[udid：%s:连接方式：%s]" % (
                            device.uid, perfdog_pb2.DEVICE_CONTYPE.Name(device.conType)))
                        stub.initDevice(device)
                        appList = stub.getAppList(device)
                        apps = appList.app
                        app = None
                        for enum_app in apps:
                            if enum_app.packageName == bundle_id:
                                LogOut.log("PerfDog找到目标监控App")
                                app = enum_app

                        LogOut.log("PerfDog获取设备的详细信息")
                        deviceInfo = stub.getDeviceInfo(device)
                        LogOut.log("PerfDog开启性能数据项")
                        stub.enablePerfDataType(
                            perfdog_pb2.EnablePerfDataTypeReq(device=device, type=perfdog_pb2.BATTERY_TEMPERATURE))
                        LogOut.log("PerfDog开始收集性能数据")
                        print(stub.startTestApp(perfdog_pb2.StartTestAppReq(device=device, app=app)))

                        break
                elif deviceEvent.eventType == perfdog_pb2.REMOVE:
                    pass
                    LogOut.log("设备[%s:%s]移除\n" % (device.uid, perfdog_pb2.DEVICE_CONTYPE.Name(device.conType)))
        except Exception as e:
            traceback.print_exc()

    def stop_monitor(self):
        """
        :return: {'AppUsage': {'value': [10.828026, 7.0536437, 10.828026, 7.0536437], 'average': 8.94}}
        """
        stub = self.stub
        device = self.device
        # stub.setLabel(perfdog_pb2.SetLabelReq(device=device, label="I am a label"))
        time.sleep(3)
        # stub.addNote(perfdog_pb2.AddNoteReq(device=device, time=5000, note="I am a note"))
        saveResult = None
        try:
            saveResult = stub.saveData(perfdog_pb2.SaveDataReq(
                device=device,
                caseName="case1",  # web上case和excel的名字
                uploadToServer=False,  # 上传到perfdog服务器
                exportToFile=True,  # 保存到本地
                outputDirectory=self.__output_dir(),
                dataExportFormat=perfdog_pb2.EXPORT_TO_JSON
            ))
        except Exception:
            LogOut.log("PerfDog保存数据时发生了异常")
            stub.stopTest(perfdog_pb2.StopTestReq(device=device))
        else:
            LogOut.log("PerfDog保存数据正常结束")
            LogOut.log("保存结果:%s" % (saveResult))
            result_file_path = saveResult.exportResult.filePath
            LogOut.log("保存结果路径:%s" % (result_file_path))
            self.result_file_path = result_file_path
            stub.stopTest(perfdog_pb2.StopTestReq(device=device))
            return self.result_file_path

    def fetch_battery_temperature_data(self, start_time_stamp, end_time_stamp):
        perf_dog_start_time = self.perf_dog_start_time
        start = start_time_stamp - perf_dog_start_time
        end = end_time_stamp - perf_dog_start_time
        if self.result_file_path is None:
            return ""
        if os.path.exists(self.result_file_path) is False:
            return ""
        with open(self.result_file_path) as json_file:
            result = json.load(json_file)
            filtered_data_list = []
            data_list = result["DataList"]
            for data in data_list:
                time_stamp = int(data["TimeStamp"])
                more_than_start = (time_stamp > start)
                less_than_end = (time_stamp < end)
                if more_than_start & less_than_end:
                    filtered_data_list.append(data)

            temperature_value = ""
            for data in filtered_data_list:
                if "BatteryTemperature" in data:
                    temperature = data["BatteryTemperature"]["BatteryTemperature"]
                    comma = "," if temperature_value else ""
                    temperature_value = temperature_value + comma + str(temperature)
            return temperature_value

    @classmethod
    def run_shell(cls, cmd):
        if cmd is None or len(cmd) < 1:
            return None
        output, error = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         bufsize=1).communicate()
        return {'output': output.decode(encoding='utf-8'), 'error': error.decode(encoding='utf-8')}

    @classmethod
    def write_values_to_log(cls, log_path, values):
        if not log_path:
            LogOut.log("没有在沙盒中找到温度模版文件")
            return

        if not os.path.exists(log_path):
            LogOut.log("没有在沙盒中找到温度模版文件路径不存在")
            return
        with open(log_path, 'r') as fp:
            json_data = json.load(fp)
            thres_hold = json_data["Detail"][0]["Result"][0]["Threshold"]
            comparison_mode = json_data["Detail"][0]["Result"][0]["ComparisonMode"]
            json_data["Detail"][0]["Result"][0]["Value"] = values
            json_data["Detail"][0]["Result"][0]["Average"] = str(Calculator.avg(values))
            json_data["Detail"][0]["Result"][0]["MaxValue"] = str(Calculator.max(values))
            json_data["Detail"][0]["Result"][0]["MinValue"] = str(Calculator.min(values))
            conclusion = "fail"
            if comparison_mode == 0:

                if float(Calculator.avg(values)) <= thres_hold:
                    conclusion = "pass"

            if comparison_mode == 1:
                if float(Calculator.avg(values)) >= thres_hold:
                    conclusion = "pass"

            json_data["Detail"][0]["Result"][0]["Conclusion"] = conclusion
            json_data["Conclusion"] = conclusion

        with open(log_path, 'w') as fp:
            json.dump(json_data, fp)

        print(json_data)

    @staticmethod
    def get_save_perf_data(result_file_path, test_log_file, test_time, device_id, bundle_id, app_name, app_version):
        """
        :param test_log_file: 测试结束日志文件
        :param task_id: 任务id
        :param test_time: 测试次数
        :param bundle_id: bundle_id
        :return:
        """
        # 先读取test_log_file, 取数据
        with open(test_log_file) as log_file:
            log_data = json.load(log_file)
            LogOut.log("get_save_perf_data log_data {}".format(log_data))
        log_file.close()
        LogOut.log("result_file_path {}".format(result_file_path))

        pd_data = json.load(open(os.path.join(result_file_path, "perfdog_metrics_json.json"), 'r'))
        perf_dog_start_time = int(pd_data["AbsDataStartTime"])
        LogOut.log("📱【pd_data】：{}".format(pd_data))
        LogOut.log("📱【device_id】：{}".format(device_id))
        LogOut.log("📱【bundle_id】：{}".format(bundle_id))
        Performance_Sql.insert_task(**{
            "device_id": device_id,
            "bundle_id": bundle_id,
            "product_name": log_data["ProductName"],
            "app_name": app_name,
            "os": log_data["OS"],
            "os_ver": log_data["OSVer"],
            "app_version": app_version,
            "device_name": log_data["DeviceName"],
            "app_build_num": log_data["AppBuildNum"],
        })

        # 按照指标 计算
        for detail in log_data.get("Detail"):
            for result in detail.get("Result"):
                test_stage_list = result["TestStageList"]
                summary_data = {}
                for test_stage in test_stage_list:
                    start = int(test_stage["Start"]) - perf_dog_start_time
                    end = int(test_stage["End"]) - perf_dog_start_time
                    if not summary_data.get(test_stage["StageIndex"]):
                        summary_data[test_stage["StageIndex"]] = {}
                    summary_data[test_stage["StageIndex"]] = get_pd_data(start, end, pd_data)
                values = []
                index = str(result["Index"])
                calculation_method = str(result["CalculationMethod"])
                calculation_stage = str(result["CalculationStage"])
                value = 0
                LogOut.log("summary_data {}".format(summary_data))
                if calculation_method == "diff" and len(calculation_stage.split(",")) == 2:  # 算stage差值的
                    stages = calculation_stage.split(",")
                    value_stage_0 = value_stage_1 = 0
                    try:
                        value_stage_0 = summary_data[str(stages[0])][index]["Average"]
                        value_stage_1 = summary_data[str(stages[1])][index]["Average"]
                    except Exception as e:
                        LogOut.log("Exception: {}".format(e))
                    value = value_stage_0 - value_stage_1
                    LogOut.log("diff: value_stage_0 {}, value_stage_1 {}, value {}".format(value_stage_0, value_stage_1, value))
                    values.append(value)
                elif calculation_method == "avg" and calculation_stage:
                    stages = calculation_stage.split(",")
                    for stage in stages:
                        average = 0
                        try:
                            average = summary_data[str(stage)][index]["Average"]
                        except Exception as e:
                            LogOut.log("Exception: {}".format(e))
                        value += average
                    value = round(value / len(stages), 2)
                    values.append(value)
                else:
                    if calculation_stage == "":
                        for test_stage in test_stage_list:
                            LogOut.log("test_stage: {} index: {}".format(test_stage["StageIndex"], index))
                            values.append(
                                ','.join(str(value) for value in
                                         summary_data[str(test_stage["StageIndex"])][index]["Value"])
                            )
                    else:
                        stages = calculation_stage.split(",")
                        for stage in stages:
                            LogOut.log("stage: {} index: {}".format(stage, index))
                            values.append(
                                ','.join(str(value) for value in
                                         summary_data[str(stage)][index]["Value"])
                            )
                LogOut.log("insert_case {}".format(detail))
                Performance_Sql.insert_case(**{
                    "test_time": test_time,
                    "device_id": device_id,
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


def get_pd_data(start_time, end_time, pd_data):
    LogOut.log("start_time {}".format(start_time))
    LogOut.log("end_time {}".format(end_time))

    summary_data = {}
    for data_list in pd_data["DataList"]:
        LogOut.log("pd_data TimeStamp {}".format(int(data_list["TimeStamp"])))
        if int(data_list["TimeStamp"]) < start_time or int(data_list["TimeStamp"]) > end_time:
            continue
        for data in data_list.values():
            if not isinstance(data, dict):
                continue
            for key, value in data.items():
                if not summary_data.get(key):
                    summary_data[key] = {
                        "Value": [],
                        "Average": 0,
                    }
                if isinstance(value, list):
                    for v in value:
                        summary_data[key]["Value"].append(float(v))
                else:
                    summary_data[key]["Value"].append(float(value))
    LogOut.log("summary_data {}".format(summary_data))
    for data in summary_data.values():
        data["Average"] = round(np.mean(data["Value"]), 2)
    return summary_data

#
# if __name__ == '__main__':
#     perfdog = PerfDog("/Volumes/workspace/goworkspace/src/tencent2/legacy/ATAPlatform/EPTestiPhoneClient/performance_test/foundation/perfdog")
#     # Performance_Sql()
#     perfdog.result_file_path = "/Volumes/workspace/goworkspace/src/tencent2/legacy/ATAPlatform/EPTestiPhoneClient/performance_test/foundation/perfdog"
#     perfdog.get_save_perf_data(perfdog.result_file_path,
#                                "/Volumes/workspace/goworkspace/src/tencent2/legacy/ATAPlatform/EPTestiPhoneClient/performance_test/foundation/perfdog/test.json", 1, "deviceid", "bundleid")
#     perf_data = Performance_Sql.gen_data("deviceid", "bundleid", "123", "QQ浏览器")
#     # data_reporter = DataReporter(False)
#     # u = json.dumps(perf_data)
# # data_reporter.report_perf_data(perf_data)
