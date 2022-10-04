# -*- coding: utf-8 -*-
from performance_test.foundation.shell import Shell


class Installer(object):

    @classmethod
    def is_install(cls, udid, bundle_id):
        app_list = cls.get_app_list(udid)
        is_install = False
        for app_name in app_list:
            print(app_name.split(",")[0])
            if bundle_id == app_name.split(",")[0]:
                is_install = True
        return is_install

    @classmethod
    def check_install(cls, udid, bundle_id, app_path):
        app_list = cls.get_app_list(udid)
        for app_name in app_list:
            if bundle_id is app_name.split(",")[0]:
                print("覆盖安装")
        return cls.install_app(udid, app_path)

    @classmethod
    def get_app_list(cls, udid):
        udid_info = Shell.run("/usr/local/bin/ideviceinstaller -u %s -l" % udid)
        out = udid_info["output"]
        out_arr = out.strip().split("\n")
        if out:
            return out_arr.pop()
        else:
            return []

    @classmethod
    def install_app(cls, udid, app_path):
        cmd = "/usr/local/bin/ideviceinstaller -u %s -i %s" % (udid, app_path)
        print("正在安装app...")
        print(cmd)
        udid_info = Shell.run(
            cmd
        )
        out = udid_info["output"]
        result = out.strip()
        print(result)
        # if "Install: Complete" in result:
        if "Complete" in result:
            print("Install: success !!")
            return True
        else:
            print("Install: Failed !!")
            return False

    @classmethod
    def uninstall_app(cls, udid, bundle_id):
        try:
            udid_info = Shell.run(
                "/usr/local/bin/ideviceinstaller -u %s -U %s" % (udid, bundle_id)
            )
            out = udid_info["output"]
            result = out.strip()
            print(result)
            if not udid_info["error"]:
                return True
            else:
                return False
        except OSError as err:
            print(err)
            return False
