import os
from performance_test.foundation.foundation_path import PathHelper as FileManager
from performance_test.proj_test.common.path import PerformancePathHelper
from tools.device_helper import DeviceHelper


class Cleaner(object):

    @classmethod
    def clean_folders(cls, udid, bundle_id):
        cls.clean_npttrail_folder_in_app(udid, bundle_id)
        cls.__clean_driver_data_and_perf_result(udid)

    @classmethod
    def clean_npttrail_folder_in_app(cls, udid, bundle_id):
        DeviceHelper.umount(PerformancePathHelper.mount_point_path(udid))
        DeviceHelper.mount(udid, bundle_id, PerformancePathHelper.mount_point_path(udid))
        FileManager.remove(os.path.join(PerformancePathHelper.mount_point_path(udid), "Documents/NPTTrail/"))
        DeviceHelper.umount(PerformancePathHelper.mount_point_path(udid))

    @classmethod
    def __clean_driver_data_and_perf_result(cls, udid):
        print("................  Clean the driver data for test")
        FileManager.clear(PerformancePathHelper.derived_data_path_for_test(udid))
