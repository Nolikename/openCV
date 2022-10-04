# ! /usr/local/bin
# -*- coding: utf-8 -*-
"""
@Time: 2022/6/24 4:33 下午
@author: jacknli
@File: video.py
@Desc: 
"""
import json
import os
import shutil
import subprocess
import time

from cloud_testing import device
from tools import report
from tools.log_out import LogOut

INIT = "init"
RUN = "run"
SETUP = "setup"


def start_record():
    device.start_record_screen()
    # for i in range(20):
    #     LogOut.log("record start")
    #     if device.start_record_screen():
    #         LogOut.log("record start success break")
    #         break


def stop_record(case_save_path, bundle_id, perf_file="", case_name="", test_time="", type=INIT,
                before_record_start=0, after_record_start=0):
    LogOut.log("💻 结束录制")
    record_result = device.stop_record_screen()

    LogOut.log("record end result: {}, {}".format(record_result.succeeded, record_result.record_screen_output_path))
    if not record_result.succeeded:
        LogOut.error("record fail: {}".format(record_result.succeeded))
        return

    if type == INIT:
        video_name = "init_{}.mp4".format(int(time.time()))
        zip_name = "init_{}_{}.zip".format(bundle_id, str(time.time()))
        video_path = os.path.join(case_save_path, video_name)
        shutil.move(record_result.record_screen_output_path, video_path)
        report.Report().upload_wetest_script_logs(case_save_path, zip_name)
        return [video_path]
    elif type == RUN:
        return video_cut(
            record_result.record_screen_output_path,
            perf_file,
            case_name,
            case_save_path,
            bundle_id,
            test_time,
            before_record_start,
            after_record_start)


def video_cut(video, perf_file, case_name, case_save_path, bundle_id, test_time, before_record_start,
              after_record_start):
    """
    :param video: 要被裁剪的视频
    :param save_video: 视频裁剪保存地址
    :param perf_file: 日志文件
    :param before_record_start: 录制命令开始前
    :param after_record_start: 录制命令开始后
    :return: 裁剪后的视频地址
    """
    if not perf_file:
        video_name = "{}_{}_{}.mp4".format(bundle_id, case_name.replace('/', '_'), test_time)
        zip_name = "run_{}_{}_{}.zip".format(bundle_id, case_name.replace('/', '_'), test_time)
        video_path = os.path.join(case_save_path, video_name)
        shutil.move(video, video_path)
        report.Report().upload_wetest_script_logs(case_save_path, zip_name)
        return [video]

    with open(perf_file) as log_file:
        log_data = json.load(log_file)
        LogOut.log("📱 log_data {}".format(log_data))
    log_file.close()
    record_stage_list = log_data.get("RecordStageList", [])
    if len(record_stage_list) <= 0:
        video_name = "{}_{}_{}.mp4".format(bundle_id, case_name.replace('/', '_'), test_time)
        zip_name = "run_{}_{}_{}.zip".format(bundle_id, case_name.replace('/', '_'), test_time)
        video_path = os.path.join(case_save_path, video_name)
        shutil.move(video, video_path)
        report.Report().upload_wetest_script_logs(case_save_path, zip_name)
        return [video]

    videos = []
    for index in range(len(record_stage_list)):
        start = record_stage_list[index]["Start"]
        end = record_stage_list[index]["End"]
        cut_start = round(int(start) / 1000.0 - after_record_start - 2.4, 2)
        cut_end = round(int(end) / 1000.0 - after_record_start + 2.4, 2)
        LogOut.log("start {}".format(start))
        LogOut.log("end {}".format(end))
        LogOut.log("cut_start {}".format(cut_start))
        LogOut.log("cut_end {}".format(cut_end))
        video_name = "{}_{}_{}_{}.mp4".format(bundle_id, case_name.replace('/', '_'), test_time, index)
        zip_name = "run_{}_{}_{}_{}.zip".format(bundle_id, case_name.replace('/', '_'), test_time, index)
        video_dir = os.path.join(case_save_path, str(index))
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)
        video_path = os.path.join(video_dir, video_name)
        cmd = "ffmpeg -i {} -ss {} -t {} -async 1 -strict -2 {}".format(
            video,
            cut_start,
            cut_end - cut_start,
            video_path)
        LogOut.log("cmd {}".format(cmd))
        subprocess.call(
            cmd,
            shell=True,
        )
        videos.append(video_path)
        report.Report().upload_wetest_script_logs(video_dir, zip_name)

    return videos
