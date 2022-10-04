# -*- coding: utf-8 -*-

import os
try:
    from pbxproj import XcodeProject
except ImportError:
    print('import error.......')
    os.system('pip3 install pbxproj')
    os.system('pip3 install xlrd')


class SignHelper(object):

    def __init__(self, pbxproj_file_path):
        self.pbxproj_file_path = pbxproj_file_path

    def mod_info_plist(self, bundle_id, info_plist_path):
       # 修改info.plist
        cmd = r"""plutil -replace CFBundleIdentifier -string "%s" %s""" % (bundle_id, info_plist_path)
        os.system(cmd)

    def mod_pbxproj_info(self, target, params):
        project = XcodeProject.load(self.pbxproj_file_path)
        root_object_pointer = project["rootObject"]
        objects = project["objects"]
        root_object = objects[root_object_pointer]
        target_pointers = root_object["targets"]

        for target_pointer in target_pointers:
            target_object = objects[target_pointer]
            if target_object["name"] != target:
                continue
            build_configuration_list_pointer = target_object["buildConfigurationList"]
            build_configuration_list_object = objects[build_configuration_list_pointer]
            build_configuration_pointers = build_configuration_list_object["buildConfigurations"]
            for build_configuration_pointer in build_configuration_pointers:
                build_configuration_object = objects[build_configuration_pointer]
                build_settings = build_configuration_object["buildSettings"]
                build_settings["PROVISIONING_PROFILE_SPECIFIER"] = params["PROVISIONING_PROFILE_SPECIFIER"]
                build_settings["CODE_SIGN_IDENTITY"] = params["CODE_SIGN_IDENTITY"]
                build_settings["PRODUCT_BUNDLE_IDENTIFIER"] = params["PRODUCT_BUNDLE_IDENTIFIER"]
                build_settings["CODE_SIGN_STYLE"] = params["CODE_SIGN_STYLE"]
                build_settings["DEVELOPMENT_TEAM"] = params["DEVELOPMENT_TEAM"]
        project.save()
