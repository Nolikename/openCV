# -*- coding: utf-8 -*-

"""
@author: ihenryhuang
@time: 2021/4/6 5:22 下午
@Copyright: Tencent. All rights reserved.

"""
import os
import json
from performance_test.foundation.ui_operator.operate_path import Path


class PerformacneUIRet(object):
    ret_code = None
    error_msg = None


class Tester(object):

    @classmethod
    def test(cls, udid, case_name, args=None):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir + "/UIOperater/UIOperaterUITests/args.json")
        # 将args写入参数json文件
        with open(json_path, "w") as file:
            json.dump(args, file)
        case_full_name = 'UIOperaterUITests/' + case_name
        test_cmd = "/Applications/Xcode.app/Contents/Developer/usr/bin/xcodebuild test "
        test_cmd += "-project " + Path.proj_path()
        test_cmd += " -scheme UIOperaterUITests "
        test_cmd += "-destination \"platform=iOS,id=" + udid + '\"'
        test_cmd += " -only-testing:"+case_full_name
        # test_cmd += " -quiet"

        ret_code = os.system(test_cmd)
        pf_ui_ret = PerformacneUIRet()
        pf_ui_ret.ret_code = ret_code
        if ret_code:
            pf_ui_ret.error_msg = case_name + "执行失败"
        else:
            pf_ui_ret.error_msg = ""
        return pf_ui_ret
