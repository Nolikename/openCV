# -*- coding: utf-8 -*-
from performance_test.foundation.xcode_sign import SignHelper
from performance_test.foundation.ui_operator.operate_path import Path as UIProjPath


class UIProjResigner(object):

    # 配置UI测试的证书
    @classmethod
    def resign(cls, params):
        pbxproj_path = UIProjPath.pbxproj_path()
        sign_helper = SignHelper(pbxproj_path)
        info_plist_path = UIProjPath.plist_path()
        sign_helper.mod_info_plist(params["PRODUCT_BUNDLE_IDENTIFIER"], info_plist_path)
        sign_helper.mod_pbxproj_info("UIOperater", params)
        sign_helper.mod_pbxproj_info("UIOperaterUITests", params)
