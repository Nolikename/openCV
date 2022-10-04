# -*- coding: utf-8 -*-
import os
import shutil
import traceback
import glob


class PathHelper(object):

    @classmethod
    def project_path(cls):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @classmethod
    def remove(cls, path):
        try:
            if os.path.exists(path) is False:
                return
            if os.path.isdir(path) is True:
                shutil.rmtree(path, True)
            else:
                os.remove(path)
        except:
            print(traceback.format_exc())
            raise ValueError('FileManager remove fail')

    @classmethod
    def clear(cls, path):
        cls.remove(path)
        try:
            os.mkdir(path)
        except OSError:
            pass

    @classmethod
    def find_all_files(cls, path):
        ret = []
        if os.path.exists(path) is False:
            return ret
        files = os.listdir(path)  # 得到文件夹下的所有文件名称

        for file in files:  # 遍历文件夹
            if not file.split('/')[-1].startswith('.') and not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                file_path = os.path.join(path, file)
                ret.append(file_path)  # 每个文件的文本存到list中
        return ret


    @classmethod
    def match_wildcard(cls, root_path="", pattern=""):
        root_path = os.path.abspath(root_path)
        results = []
        for root, _, _ in os.walk(root_path):
            for match in glob.glob(os.path.join(root, pattern)):
                results.append(match)
        return results
