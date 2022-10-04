# -*- coding: utf-8 -*-
"""
@Time: 2022/3/7 下午3:24
@author: jacknli
@File: file.py
@Desc: 文件操作方法
"""
from logzero import logger
import subprocess
import tarfile
import zipfile
import urllib
from threading import Timer

from performance_test.foundation.marked.marked_calculate import __get_img_data
from performance_test.foundation.marked.tpl_match import tpl_match


def untar(file_name, file_path):
    """
    unzip *.tar.gz

    :param file_name:  压缩文件名
    :param file_path: 解压存放文件夹路径
    """
    try:
        if str(file_name).endswith((".tar", ".tar.gz")):
            t = tarfile.open(file_name)
            t.extractall(path=file_path)
        elif str(file_name).endswith(".zip"):
            zip_files = zipfile.ZipFile(file_name)
            for zip_file in zip_files.namelist():
                zip_files.extract(zip_file, file_path)
            zip_files.close()
    except tarfile.ExtractError as e:
        print(e)


def download_file(download_url, file_path):
    """
    download http url file

    :param download_url: url
    :param file_path: file path with name
    """
    try:
        urllib.urlretrieve(download_url, file_path)
    except Exception as e:
        print(e)


def proc_trace(timeout, proc):
    timer = Timer(timeout, proc.kill)
    try:
        timer.start()
        stdout, stderr = proc.communicate()
    finally:
        timer.cancel()
    logger.info("stdout: {}, stderr: {}, proc.returncode: {}".format(stdout, stderr, proc.returncode))
    return proc.returncode


if __name__ == '__main__':
    from performance_test.foundation.cv.cv_analyzer import cv_analyse
    from performance_test.foundation.marked.marked_params import MarkedParams, DivideFrameMode, MarkedStrategy

    #
    # params = MarkedParams()
    # params.set_divide_frame_mode(DivideFrameMode.FFMPEG)
    # params.add_start_marked_img_path("/Users/lining/Downloads/0/start.png")
    # params.add_end_marked_img_path("/Users/lining/Downloads/0/end.png")
    # params.add_end_marked_img_path("/Users/lining/Downloads/0/endSearchHot.png")
    # start_position = False
    # params.set_start_marked_strategy(MarkedStrategy.AND)
    # params.set_end_marked_strategy(MarkedStrategy.OR)
    # params.set_start_marked_use_appear(start_position)
    # result = cv_analyse("/Users/lining/Downloads/0/test.mp4", params)
    # if not start_position:
    #     result = result + 0.0167
    # print(result)
    proc = subprocess.Popen("/usr/bin/python3 /Volumes/workspace/goworkspace/src/tencent2/legacy/ATAPlatform/EPTestiPhoneClient/performance_test/testCV.py --pic_dir='a'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    proc_trace(30, proc)
