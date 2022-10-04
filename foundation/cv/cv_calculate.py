# ! /usr/local/bin
# -*- coding: utf-8 -*-
"""
@Time: 2022/8/10 4:19 PM
@author: jacknli
@File: cv_calculate.py
@Desc: 
"""
import sys

sys.path.append(".")

# 图像识别加载速度
import argparse
import os
import shutil
from enum import Enum

from loguru import logger

from foundation.cv.cv_analyzer import load_analyzer
from foundation.cv.video_frame_util import video_to_frames_with_ffmpeg
from foundation.cv.video_frame_util import video_to_frames_with_opencv
from foundation.marked.marked_calculate import get_marked_img_position
from foundation.marked.marked_params import MarkedParams, MarkedResult, MarkedStrategy
from foundation.marked.marked_params import DivideFrameMode

# 用于毫米转为秒
FLOAT_1000 = 1000.0

VIDEO_MP4 = ".mp4"
VIDEO_MKV = ".mkv"
START_PIC = "start"
END_PIC = "end"
FALSE = "False"


def cv_analyse(video_path: str, marked_paras: MarkedParams):
    default_frames_dir, fps = video_to_frames(video_path, marked_paras)
    for path, dir_list, file_list in os.walk(default_frames_dir):
        logger.info(f"cv_analyse 一共 {len(file_list)} 个视频帧画面")
    if marked_paras:
        start_marked_size = len(marked_paras.get_start_marked_img_path_list())
        end_marked_size = len(marked_paras.get_end_marked_img_path_list())
        marked_paras.set_video_path(video_path)
        if start_marked_size > 0 and end_marked_size > 0:
            # 完全依赖标注分析
            marked_result = get_marked_img_position(marked_paras, default_frames_dir)
            result = calculate_load_time(marked_paras, marked_result)
        elif start_marked_size == 0 and end_marked_size == 0:
            # 先使用标注识别确定开始帧或结束帧，再过滤掉使用图像识别推导
            result = load_analyzer(default_frames_dir, marked_paras.get_divide_frame_mode(), fps)
        else:
            result = mixed_analyse(marked_paras, default_frames_dir, marked_paras.get_divide_frame_mode(), fps)
    else:
        result = load_analyzer(default_frames_dir, marked_paras.get_divide_frame_mode(), fps)
    # clear_temp_file(default_frames_dir)
    return result


def video_to_frames(video_path: str, marked_paras: MarkedParams):
    if marked_paras.get_divide_frame_mode() == DivideFrameMode.FFMPEG:
        return video_to_frames_with_ffmpeg(video_path, marked_paras.get_divide_frame_fps())
    else:
        return video_to_frames_with_opencv(video_path)


def mixed_analyse(marked_paras: MarkedParams, default_frames_dir: str, frame_mode: Enum, fps: int) -> float:
    marked_result = get_marked_img_position(marked_paras, default_frames_dir)
    if not marked_result.status:
        logger.error(marked_result.fail_msg)
        return -1.0
    if len(marked_result.get_first_frame_index_list()):
        # result页面加载完成时所消耗的时间（把start_index作为起点）
        result = load_analyzer(default_frames_dir, frame_mode, fps, marked_result.get_start_marked_pos(), 0)
        if marked_paras.get_divide_frame_mode() == DivideFrameMode.FFMPEG:
            start_time = marked_result.get_first_frame_index_list()[0] * 1.0 / marked_paras.get_divide_frame_fps()
        else:
            # 单位由毫米统一转为秒
            start_time = marked_result.get_first_frame_index_list()[0] / FLOAT_1000
        logger.info(f'mixed_analyse | start frame time:{start_time}s, end frame time:{start_time + result}s')
        return result

    if len(marked_result.get_last_frame_index_list()):
        if marked_paras.get_divide_frame_mode() == DivideFrameMode.FFMPEG:
            end_time = marked_result.get_last_frame_index_list()[0] * 1.0 / marked_paras.get_divide_frame_fps()
        else:
            # 单位由毫米统一转为秒
            end_time = marked_result.get_last_frame_index_list()[0] / FLOAT_1000
        if end_time < 0:
            end_time = load_analyzer(default_frames_dir, frame_mode, fps, 0, marked_result.get_end_marked_pos())
        logger.info(f'mixed_analyse | 这种方式适用冷启动带启动页场景（启动页带Logo图像作为起始点）')
        logger.info(f'mixed_analyse | start frame time:0s, end frame time:{end_time}s')
        return end_time
    return -1


# 通过帧差，除以帧率，获取耗时,单位秒
def calculate_load_time(marked_paras: MarkedParams, marked_result: MarkedResult) -> float:
    if not marked_result.status:
        logger.error(marked_result.fail_msg)
        return -1.0
    start_index = marked_result.get_first_frame_index_list()[0]
    end_index = marked_result.get_last_frame_index_list()[0]
    if start_index == -1 or end_index == -1:
        return -1.0
    if marked_paras.get_divide_frame_mode() == DivideFrameMode.FFMPEG:
        start_time = start_index * FLOAT_1000 / marked_paras.get_divide_frame_fps()
        end_time = end_index * FLOAT_1000 / marked_paras.get_divide_frame_fps()
        result = (end_index - start_index) * FLOAT_1000 / marked_paras.get_divide_frame_fps()
    else:
        # 单位由毫米统一转为单位秒
        start_time = start_index
        end_time = end_index
        result = (end_index - start_index)
    logger.info(f'start frame time:{start_time}ms')
    logger.info(f'end frame time:{end_time}ms')
    logger.info(f'result:{result}ms')
    return result


def clear_temp_file(temp_path: str):
    del_list = os.listdir(temp_path)
    for f in del_list:
        file_path = os.path.join(temp_path, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def build_marked_params(file_path, start_strategy=False, end_strategy=False, start_use_appear=False,
                        end_use_appear=False, start_point_marked=False, frame_mode=False, fps=60) -> MarkedParams:
    """
    构造MarkedParams
    :param file_path: 素材文件路径
    :param start_strategy: start_strategy
    :param end_strategy: end_strategy
    :param start_use_appear: start_use_appear
    :param end_use_appear: end_use_appear
    :param start_point_marked: start_point_marked
    :param frame_mode: 切帧方式
    :param fps: fps
    :return: MarkedParams
    """
    print(start_strategy, end_strategy, start_use_appear, end_use_appear, start_point_marked, frame_mode, fps)
    marked_param = MarkedParams()
    if start_strategy:
        marked_param.set_start_marked_strategy(MarkedStrategy.AND)
    else:
        marked_param.set_start_marked_strategy(MarkedStrategy.OR)

    if end_strategy:
        marked_param.set_end_marked_strategy(MarkedStrategy.AND)
    else:
        marked_param.set_end_marked_strategy(MarkedStrategy.OR)

    if not start_use_appear:
        marked_param.set_start_marked_use_appear(start_use_appear)

    if not end_use_appear:
        marked_param.set_end_marked_use_appear(end_use_appear)

    if not start_point_marked:
        marked_param.set_point_position_marked(start_point_marked)

    start_pics = get_pics(file_path, START_PIC)
    for pic in start_pics:
        marked_param.add_start_marked_img_path(pic)

    end_pics = get_pics(file_path, END_PIC)
    for pic in end_pics:
        marked_param.add_end_marked_img_path(pic)

    if frame_mode:
        marked_param.set_divide_frame_mode(DivideFrameMode.OPENCV, fps=fps)
    else:
        marked_param.set_divide_frame_mode(DivideFrameMode.FFMPEG, fps=fps)

    return marked_param


def get_pics(path: str, mode: str):
    """
    获取素材图片
    :param path: 路径
    :param mode: 前缀
    :return: file_list
    """
    file_list = []
    for root, _, files in os.walk(path):
        for f in files:
            if not f.startswith(mode):
                continue
            f_dir = os.path.join(root, f)
            file_list.append(f_dir)
    return file_list


def write_result(result, path):
    with open(os.path.join(path, "result.txt"), 'a') as result_file:
        result_file.write(result)
    result_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video",
        dest="video",
        help="path 被分析的包含视频和素材图片文件夹",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--path",
        dest="path",
        help="path 素材图片文件夹",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--start_strategy",
        dest="start_strategy",
        help="start_strategy ",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--end_strategy",
        dest="end_strategy",
        help="end_strategy ",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--start_use_appear",
        dest="start_use_appear",
        help="start_use_appear ",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--end_use_appear",
        dest="end_use_appear",
        help="end_use_appear ",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--start_point_marked",
        dest="start_point_marked",
        help="start_point_marked ",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--frame_mode",
        dest="frame_mode",
        help="frame_mode ",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--fps",
        dest="fps",
        help="fps ",
        type=int,
        required=False,
    )

    args = parser.parse_args()
    args_dict = vars(args)
    if not os.path.isdir(args_dict.get("path")):
        logger.error("path not dir")
        sys.exit()
    elif not os.path.exists(args_dict.get("video")):
        logger.error("path not dir")
        sys.exit()

    params = build_marked_params(
        args_dict.get("path"),
        False if args_dict.get("start_strategy") == FALSE else True,
        False if args_dict.get("end_strategy") == FALSE else True,
        False if args_dict.get("start_use_appear") == FALSE else True,
        False if args_dict.get("end_use_appear") == FALSE else True,
        False if args_dict.get("start_point_marked") == FALSE else True,
        False if args_dict.get("frame_mode") == FALSE else True,
        60 if not args_dict.get("fps") else args_dict.get("fps"),
    )

    video_result = cv_analyse(args_dict.get("video"), params)
    if video_result > 0:
        write_result(str(video_result) + '\n', args_dict.get("path"))
