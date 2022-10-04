# -*- coding: utf-8 -*-
import os
import shutil
import traceback


class FileManager(object):
    @classmethod
    def remove(cls, path):
        try:
            if os.path.exists(path) is False:
                return
            if os.path.isdir(path) is True:
                shutil.rmtree(path)
            else:
                os.remove(path)
        except OSError:
            print(traceback.format_exc())

    @classmethod
    def clean(cls, path):
        if not os.path.exists(path):
            return
        # 清空文件夹
        FileManager.remove(path)
        os.makedirs(path)

    @classmethod
    def copy_files_in_folder(cls, source_folder, target_folder):
        files = os.listdir(source_folder)
        for file in files:
            source_path = os.path.join(source_folder, file)
            target_path = os.path.join(target_folder, file)
            shutil.copytree(source_path, target_path)

    @classmethod
    def project_path(cls):
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    @classmethod
    def find_all_files(cls, path):
        files = os.listdir(path)  # 得到文件夹下的所有文件名称
        result = []
        for file in files:  # 遍历文件夹
            if not file.startswith('.') and not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                file_path = os.path.join(path, file)
                result.append(file_path)  # 每个文件的文本存到list中
        return result
