# coding=utf-8
import ctypes
import os
import shutil
import subprocess

# 视频转图像帧
import cv2
from logzero import logger

from foundation.marked.marked_params import DivideFrameMode


def __get_default_frames_dir(video_path):
    # 视频所在目录文件夹名称
    return '{}/frames/'.format(os.path.dirname(video_path))


def video_to_frames_with_ffmpeg(video_path, fps):
    """
    使用ffmpeg进行视频分帧
    Args:
        video_path: 视频地址
        fps: 指定视频分帧fps
    Returns:
        第一个返回值：分帧后文件所在文件夹地址
        第二个返回值：分帧fps值
    """

    # 视频所在目录文件夹名称
    default_frames_dir = __get_default_frames_dir(video_path)
    if os.path.exists(default_frames_dir):
        shutil.rmtree(default_frames_dir)
    os.makedirs(default_frames_dir)

    logger.info("start video to frames")
    cut_video_command = "ffmpeg -i {}  -r {}  -q:v 2 -f image2 {}%08d.png"
    logger.info(cut_video_command.format(video_path, fps, default_frames_dir))
    p = subprocess.Popen(cut_video_command.format(video_path, fps, default_frames_dir),
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    # 阻塞调用, 等待视频分帧结束
    p.communicate()
    logger.info("end video to frames")
    return default_frames_dir, fps


def video_to_frames_with_opencv(video_path, reset_height = 0):
    """
    将视频转换成一帧帧的图片
    video_path: 视频文件完整路径
    default_frames_dir: 视频分帧后存放文件路径
    reset_height: 图片高度重设为指定值，0 表示不重设
    """
    # 读入视频文件
    vc = cv2.VideoCapture(video_path)
    # 判断视频文件是否读取成功
    flag = vc.isOpened()
    if not flag:
        logger.error("open input file error!")
        return None
    default_frames_dir = __get_default_frames_dir(video_path)
    if not os.path.exists(default_frames_dir):
        os.makedirs(default_frames_dir)
    # 获取视频的帧率，即一秒钟该视频播放多少帧
    fps = vc.get(cv2.CAP_PROP_FPS)
    width = vc.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = vc.get(cv2.CAP_PROP_FRAME_HEIGHT)
    frames_count = vc.get(cv2.CAP_PROP_FRAME_COUNT)
    logger.info(
        'fps={} , width={} , height={} , frames_count={} ，total_time={}'.format(
            fps, width, height, frames_count, frames_count / fps
        ))
    prev_frame_pos_msec = 0
    frame_pos_msec = 0
    while True:
        frame_exists, curr_frame = vc.read()
        # 如果已经读取到最后一帧则退出
        if not frame_exists:
            break
        if reset_height > 0 and reset_height != curr_frame.shape[0]:
            new_width = reset_height * curr_frame.shape[1] / curr_frame.shape[0]
            width = int(new_width)
            height = int(reset_height)
            dim = (width, height)
            curr_frame = cv2.resize(curr_frame, dim, interpolation=cv2.INTER_AREA)

        # 通过视频帧的位置时间计算索引frame_index
        frame_pos_msec = vc.get(cv2.CAP_PROP_POS_MSEC)
        # ignore useless frames
        if frame_pos_msec < prev_frame_pos_msec:
            continue
        prev_frame_pos_msec = frame_pos_msec
        frame_index = int(round(frame_pos_msec))
        cv2.imwrite(os.path.join(default_frames_dir, str(frame_index).zfill(8) + '.png'), curr_frame)
    vc.release()
    return default_frames_dir, fps
