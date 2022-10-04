# -*- coding: utf-8 -*-
from ataplatform_base import logger
from performance_test.foundation.ui_operator.operate_test import Tester as UItester


class UIProcessor(object):

    @classmethod
    def process_if_needed(cls, case_name, udid):
        case_name = case_name
        if case_name.endswith("_bus"):
            cls.__net_bus(udid)
            return True
        if case_name.endswith("_railway"):
            cls.__net_railway(udid)
            return True
        if case_name.endswith("_subway"):
            cls.__net_subway(udid)
            return True
        if case_name.endswith("_launch"):
            cls.__launch(udid)

    @classmethod
    def tap_all_alert(cls, udid):
        # 点击所有的弹窗
        logger.info("弹窗处理")
        ret1 = UItester.test(udid, "Alert/testHandleAlert1")
        print("Alert/testHandleAlert1 excute result %s", ret1)
        ret2 = UItester.test(udid, "Alert/testHandleAlert2")
        print("Alert/testHandleAlert2 excute result %s", ret2)
        ret3 = UItester.test(udid, "Alert/testHandleAlert3")
        print("Alert/testHandleAlert3 excute result %s", ret3)
        ret4 = UItester.test(udid, "Alert/testHandleAlert4")
        print("Alert/testHandleAlert4 excute result %s", ret4)

    @classmethod
    def __launch(cls, udid):
        logger.info("连续启动中...")
        UItester.test(udid, "Launch/testLaunch")
        logger.info("连续启动结束")

    @classmethod
    def __net_bus(cls, udid):
        logger.info("配置巴士网络")
        UItester.test(udid, "NetworkLinkConditioner/testBus")

    @classmethod
    def __net_railway(cls, udid):
        logger.info("配置铁路网络")
        UItester.test(udid, "NetworkLinkConditioner/testRailway")

    @classmethod
    def __net_subway(cls, udid):
        logger.info("配置地铁网络")
        UItester.test(udid, "NetworkLinkConditioner/testSubway")

    @classmethod
    def net_disable(cls, udid):
        logger.info("关闭弱网")
        UItester.test(udid, "NetworkLinkConditioner/testDisable")
