# ! /usr/local/bin
# -*- coding: utf-8 -*-
"""
@Time: 2022/3/22 下午3:35
@author: jacknli
@File: sql.py
@Desc:
"""
import math
import os
import re
import shutil
import sqlite3
import time

import numpy as np
from ataplatform_base import logger

from tools import plist_helper

TABLENAME = "performance.db"
DBNAME = "PERFORMANCE"
DBPATH = os.path.join(os.getcwd(), TABLENAME)


# 浮点数小数点精度
FLOAT_PRECISION = 3
FAIL = "fail"
PASS = "pass"


# 性能本地执行数据库
class Performance_Sql(object):
    def __init__(self):
        self.delete_sql()
        self.__create_table()

    @staticmethod
    def delete_sql():
        if os.path.exists(DBPATH):
            os.remove(DBPATH)

    @classmethod
    def __create_table(cls):
        """
        创建任务表和用例表
        """
        logger.info("DBPATH: {}".format(DBPATH))
        conn = sqlite3.connect(DBPATH)
        logger.info("性能数据库打开成功")
        c = conn.cursor()
        c.execute('''CREATE TABLE PERFORMANCE_CASE
               (id INTEGER PRIMARY KEY  NOT NULL,
                test_time INT NOT NULL,
                device_id VARCHAR(255) NOT NULL,
                bundle_id VARCHAR(255) NOT NULL,
                case_name VARCHAR(255) NOT NULL,
                index_name VARCHAR(255) NOT NULL,
                app_name VARCHAR(255) NOT NULL,
                value TEXT NOT NULL,
                threshold FLOAT NOT NULL,
                threshold_up FLOAT NOT NULL,
                threshold_down FLOAT NOT NULL,
                comparison_mode INT NOT NULL,
                unit VARCHAR(50) NOT NULL,
                computing_percent INT NOT NULL);''')
        c.execute('''CREATE INDEX case_info_index1 ON PERFORMANCE_CASE (bundle_id, case_name, index_name);''')
        c.execute(
            '''CREATE INDEX case_info_index2 ON PERFORMANCE_CASE (device_id, bundle_id, case_name, index_name);''')
        c.execute('''CREATE TABLE PERFORMANCE_TASK
                            (id INTEGER PRIMARY KEY  NOT NULL,
                            device_id VARCHAR(255) NOT NULL,
                            bundle_id VARCHAR(255) NOT NULL,
                            product_name  VARCHAR(255) NOT NULL,
                            app_name VARCHAR(255) NOT NULL,
                            os VARCHAR(255) NOT NULL,
                            os_ver VARCHAR(255) NOT NULL,
                            app_version VARCHAR(255) NOT NULL,
                            device_name VARCHAR(255) NOT NULL,
                            app_build_num INT NOT NULL);''')
        c.execute('''CREATE INDEX task_info_index1 ON PERFORMANCE_TASK (bundle_id);''')
        c.execute('''CREATE INDEX task_info_index2 ON PERFORMANCE_TASK (device_id, bundle_id);''')
        logger.info("性能数据表创建成功")
        conn.commit()
        conn.close()

    @classmethod
    def insert_case(cls, **kwargs):
        """
        用例插入
        :param kwargs:
        """
        logger.info(kwargs)
        logger.info(DBPATH)
        conn = sqlite3.connect(DBPATH)
        c = conn.cursor()
        logger.info("数据库打开成功")
        sql = "INSERT INTO PERFORMANCE_CASE (" \
              "test_time,device_id,bundle_id,case_name,index_name,app_name,value,threshold," \
              "threshold_up,threshold_down,comparison_mode,unit,computing_percent) " \
              "VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')" \
            .format(kwargs["test_time"], kwargs["device_id"], kwargs["bundle_id"],
                    kwargs["case_name"], kwargs["index_name"], kwargs["app_name"], kwargs["value"], kwargs["threshold"],
                    kwargs["threshold_up"], kwargs["threshold_down"], kwargs["comparison_mode"],
                    kwargs["unit"], kwargs["computing_percent"])
        print(sql)
        c.execute(sql)
        conn.commit()
        logger.info("数据插入成功")
        conn.close()

    @classmethod
    def insert_task(cls, **kwargs):
        """
        任务插入
        :param kwargs:
        :return:
        """
        logger.info(kwargs)
        logger.info(DBPATH)
        conn = sqlite3.connect(DBPATH)
        c = conn.cursor()
        logger.info("数据库打开成功")
        cursor = c.execute(
            "SELECT count(*) from PERFORMANCE_TASK WHERE device_id = '{}' AND bundle_id = '{}' AND app_name = '{}'".format(
                kwargs["device_id"], kwargs["bundle_id"], kwargs["app_name"]))
        for cur in cursor:
            if cur[0] >= 1:
                logger.info("exists")
                return
        c.execute("INSERT INTO PERFORMANCE_TASK (device_id,bundle_id,product_name,"
                  "app_name,os,os_ver,app_version,device_name,app_build_num) \
              VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            kwargs["device_id"], kwargs["bundle_id"], kwargs["product_name"],
            kwargs["app_name"], kwargs["os"], kwargs["os_ver"],
            kwargs["app_version"], kwargs["device_name"], kwargs["app_build_num"]))
        conn.commit()
        logger.info("数据插入成功")
        conn.close()

    @classmethod
    def get_case_info(cls, cur):
        case_info = {
            "test_time": cur[1],
            "device_id": cur[2],
            "bundle_id": cur[3],
            "case_name": cur[4],
            "index_name": cur[5],
            "app_name": cur[6],
            "value": cur[7],
            "threshold": cur[8],
            "threshold_up": cur[9],
            "threshold_down": cur[10],
            "comparison_mode": cur[11],
            "unit": cur[12],
            "computing_percent": cur[13],
        }
        return case_info

    @classmethod
    def get_index_infos(cls, device_id, bundle_id, app_name, case_name, index_name):
        logger.info("📱【device_id】：{}".format(device_id))
        logger.info("📱【bundle_id】：{}".format(bundle_id))
        logger.info("📱【app_name】：{}".format(app_name))
        logger.info("📱【case_name】：{}".format(case_name))
        logger.info("📱【index_name】：{}".format(index_name))
        conn = sqlite3.connect(DBPATH)
        c = conn.cursor()
        logger.info("数据库打开成功")
        cursor = c.execute(
            "SELECT * from PERFORMANCE_CASE WHERE device_id = '{}' AND bundle_id = '{}' AND app_name = '{}' "
            "AND case_name = '{}' AND index_name = '{}'".format(device_id, bundle_id, app_name, case_name, index_name))
        index_list = []
        for cur in cursor:
            index_list.append(cls.get_case_info(cur))
        logger.info("📱【index_list】：{}".format(index_list))
        return index_list

    @classmethod
    def get_cases(cls, device_id, bundle_id):
        """
        获取db里边, 用例名和指标名
        :return:
        """
        logger.info("📱【device_id】：{}".format(device_id))
        logger.info("📱【bundle_id】：{}".format(bundle_id))
        conn = sqlite3.connect(DBPATH)
        c = conn.cursor()
        logger.info("数据库打开成功")
        cursor = c.execute(
            "SELECT DISTINCT case_name from PERFORMANCE_CASE "
            "WHERE device_id = '{}' AND bundle_id = '{}'".format(device_id, bundle_id))
        cases = []
        for cur in cursor:
            cases.append(cur[0])
        logger.info("📱【get_cases】：{}".format(cases))
        return cases

    @classmethod
    def get_indexs(cls, device_id, bundle_id, app_name, case_name):
        """
        获取db里边, 用例名和指标名
        :return:
        """
        logger.info("📱【device_id】：{}".format(device_id))
        logger.info("📱【bundle_id】：{}".format(bundle_id))
        logger.info("📱【app_name】：{}".format(app_name))
        logger.info("📱【case_name】：{}".format(case_name))
        conn = sqlite3.connect(DBPATH)
        c = conn.cursor()
        logger.info("数据库打开成功")
        cursor = c.execute(
            "SELECT DISTINCT index_name, computing_percent from PERFORMANCE_CASE "
            "WHERE device_id = '{}' AND bundle_id = '{}' AND app_name = '{}' AND case_name = '{}'".format(
                device_id, bundle_id, app_name, case_name))
        indexs = []
        for cur in cursor:
            indexs.append({
                "index_name": cur[0],
                "computing_percent": cur[1],
            })
        logger.info("📱【get_indexs】：{}".format(indexs))
        return indexs

    @classmethod
    def get_task(cls, device_id, bundle_id, app_name):
        logger.info("📱【device_id】：{}".format(device_id))
        logger.info("📱【bundle_id】：{}".format(bundle_id))
        logger.info("📱【app_name】：{}".format(app_name))
        logger.info("📱【DBPATH】：{}".format(DBPATH))
        conn = sqlite3.connect(DBPATH)
        c = conn.cursor()
        logger.info("数据库打开成功")
        cursor = c.execute(
            "SELECT * from PERFORMANCE_TASK WHERE device_id = '{}' AND bundle_id = '{}' AND app_name = '{}' ".format(
                device_id, bundle_id, app_name))
        for cur in cursor:
            print(cur)
            task_info = {
                "device_id": cur[1],
                "bundle_id": cur[2],
                "product_name": cur[3],
                "app_name": cur[4],
                "os": cur[5],
                "os_ver": cur[6],
                "app_version": cur[7],
                "device_name": cur[8],
                "app_build_num": cur[9],
            }
            conn.close()
            logger.info("📱【get_task】：{}".format(task_info))
            return task_info

    @classmethod
    def gen_data(cls, device_id, bundle_id, triger_id, app_name):
        """
        从db拿所有的数据，并组装
        :param device_id: 设备id
        :param bundle_id: app bundle id
        :param triger_id: 任务id
        :return:
        """
        task_result = cls.gen_task(cls.get_task(device_id, bundle_id, app_name))
        cases = cls.get_cases(device_id, bundle_id)
        case_result_conclusion = PASS
        for case in cases:
            case_result = cls.gen_case(case)
            indexs = cls.get_indexs(device_id, bundle_id, app_name, case)
            for index in indexs:
                index_infos = cls.get_index_infos(device_id, bundle_id, app_name, case, index["index_name"])
                values = []
                for index_info in index_infos:
                    values.append(index_info["value"])
                # 计算values相关
                case_result["Result"].append(cls.gen_index(index_infos[0], values))
            for result in case_result["Result"]:
                if result["Conclusion"] == FAIL:
                    case_result["Conclusion"] = FAIL
                    case_result_conclusion = FAIL
                    break

            task_result["Detail"].append(case_result)
        task_result["TaskId"] = str(triger_id)
        task_result["DeviceId"] = device_id
        task_result["Conclusion"] = case_result_conclusion
        logger.info("task_result: {}".format(task_result))
        return {
            "CompetitorPerfInfo": task_result
        }

    @staticmethod
    def get_percent_average(values, percent):
        """
        计算分位值，默认percent 0 为均值
        :param values: [12,21,24,32,43,45,50,53,55,56,58,60]
        :param percent: 90
        :return: 57.8
        """
        if percent <= 0 or percent >= 100:
            return round(np.mean(values), 2)
        values.sort()
        size = round(float(len(values) - 1) / 100.0, 2)
        position = size * percent
        floor = int(math.floor(position))
        value = values[floor] + (values[floor + 1] - values[floor]) * (position - floor)
        print("{} percent value is {}".format(percent, value))
        return value

    @staticmethod
    def gen_task(task_info):
        task = {
            "ProductName": task_info["product_name"],
            "OS": task_info["os"],
            "OSVer": task_info["os_ver"],
            "AppName": task_info["app_name"],
            "AppVersion": task_info["app_version"],
            "AppBuildNum": task_info["app_build_num"],
            "DeviceName": task_info["device_name"],
            "VideoKey": "",
            "Conclusion": PASS,
            "Detail": []
        }
        logger.info("📱【task_info】：{}".format(task_info))
        return task

    @staticmethod
    def gen_case(case_name):
        case = {
            "CaseName": case_name,
            "Conclusion": PASS,
            "Result": [],
        }
        return case

    @staticmethod
    def gen_index(index_info, values):
        result = {
            "MaxValue": "0.00",
            "Cause": "-",
            "Name": index_info["index_name"],
            "ThresholdUp": int(index_info["threshold_up"]),
            "Threshold": int(index_info["threshold"]),
            "ThresholdDown": int(index_info["threshold_down"]),
            "Average": "0.00",
            "MinValue": "0.00",
            "ComparisonMode": index_info["comparison_mode"],
            "Unit": index_info["unit"],
            "Conclusion": PASS,
            "Type": "string",
            "Value": "",
            "HideChat": 0
        }

        perf_values = []
        for vals in values:
            if vals == '':
                continue
            val = vals.split(",")
            for v in val:
                perf_values.append(float(v))
        if len(perf_values) <= 0:
            result["Value"] = ''
            result["MaxValue"] = "0"
            result["MinValue"] = "0"
        else:
            result["Value"] = ','.join(map(str, perf_values))
            result["MaxValue"] = str(np.max(perf_values))
            result["MinValue"] = str(np.min(perf_values))

        average = get_average(perf_values, index_info["computing_percent"])
        result["Average"] = str(average)
        if result["Threshold"] < 0:
            return

        if result["ComparisonMode"] and float(result["Average"]) < float(result["Threshold"]):
            result["Conclusion"] = FAIL

        if not result["ComparisonMode"] and float(result["Average"]) > float(result["Threshold"]):
            result["Conclusion"] = FAIL

        result["Cause"] = build_cause(
            result["Conclusion"],
            float(index_info["threshold"]),
            average,
            result["Unit"],
            result["ComparisonMode"]
        )
        return result

# 构建失败原因
def build_cause(conclusion, threshold, average, unit, comparison_mode):
    if conclusion != FAIL:
        return '-'
    diff_value = round(abs(threshold - average), FLOAT_PRECISION)
    percentage_value = round((diff_value / float(threshold)) * 100, FLOAT_PRECISION)
    logger.error("diff_value:{} / percentage_value:{}".format(diff_value, percentage_value))
    cause = ''
    if unit == 'KB/s':
        cause = "网络下行有增量"
    elif unit == "%":
        cause = "均值低于阈值{}个百分比, 相对阈值低出: {}%".format(diff_value, percentage_value) \
            if comparison_mode else "均值超过阈值{}个百分比, 相对阈值高出: {}%".format(diff_value, percentage_value)
    else:
        cause = "均值小于阈值: {}{}, 相对阈值低出: {}%".format(diff_value, unit, percentage_value) \
            if comparison_mode else "均值大于阈值: {}{}, 相对阈值高出: {}%".format(diff_value, unit, percentage_value)
    return cause


def get_average(values, percent):
    """
    计算分位值，默认percent 0 为均值
    :param values: [12,21,24,32,43,45,50,53,55,56,58,60]
    :param percent: 90
    :return: 57.8
    """
    if len(values) <= 0:
        return 0
    if percent <= 0 or percent >= 100:
        return round(np.mean(values), 2)
    if len(values) == 1:
        return values[0]
    values.sort()
    size = round(float(len(values) - 1) / 100.0, 2)
    position = size * percent
    floor = int(math.floor(position))
    value = values[floor] + (values[floor + 1] - values[floor]) * (position - floor)
    print("{} percent value is {}".format(percent, value))
    return value


def copy_db_file(destination_path):
    """
    拷贝db文件
    :param destination_path: 目的路径
    """

    save_path = os.path.join(destination_path, DBNAME)
    logger.info("save_path: {}, DBPATH: {}".format(save_path, DBPATH))
    shutil.rmtree(save_path, True)
    shutil.copy(DBPATH, save_path)
