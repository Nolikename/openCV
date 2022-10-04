import ctypes
import os.path
import platform
import shutil
from enum import Enum

from loguru import logger

PLATFORM_MAC = "Darwin"
PLATFORM_LINUX = "Linux"
PLATFORM_WIN = "Windows"

WINDOW_LIBS = ['msvcp140d.dll', 'ucrtbased.dll', 'vcruntime140d.dll', 'vcruntime140_1d.dll', 'concrt140d.dll']


def pre_check():
    system_path = os.path.join('C:\\', 'Windows', 'System32')
    if os.path.exists(system_path):
        for lib in WINDOW_LIBS:
            lib_file_path = os.path.join(system_path, lib)
            if not os.path.exists(lib_file_path):
                curr_lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'win', lib)
                logger.info(f'Copy System Lib {lib} To System32 Dir {lib_file_path}')
                try:
                    # 将指定的文件file复制到file_dir的文件夹里面
                    shutil.copy(curr_lib_path, system_path)
                except IOError as e:
                    logger.info(f'Unable to copy file error:{e}')
    else:
        logger.error("Find System Window32 Dir Fail")


def load_analyzer(default_frames_dir: str, frame_mode: Enum, fps: int, start_index: int = 0,
                  end_index: int = 0) -> float:
    os_platform = platform.system()
    logger.info(f'os_platform = {os_platform}  path exist:{os.path.exists(default_frames_dir)}')
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    if os_platform == PLATFORM_MAC:
        # Mac库文件的路径 ,需要执行 brew install opencv
        lib = ctypes.cdll.LoadLibrary(os.path.join(parent_dir, 'mac', 'libanalyse_frame.dylib'))
    elif os_platform == PLATFORM_LINUX:
        # linux库文件的路径
        lib = ctypes.cdll.LoadLibrary(os.path.join(parent_dir, 'linux', 'libanalyse_frame.so'))
    elif os_platform == PLATFORM_WIN:
        pre_check()
        # windows库文件的路径
        lib = ctypes.windll.LoadLibrary(os.path.join(parent_dir, 'win', 'libanalyse_frame.dll'))
        if default_frames_dir.endswith('/'):
            default_frames_dir = default_frames_dir[::-1].replace('/', '', 1)[::-1]
    else:
        logger.error("不支持目前系统")
        return

    # 设置返回值的转义
    lib.analyse.restype = ctypes.c_double

    sn = ctypes.create_string_buffer(default_frames_dir.encode('utf-8'), len(default_frames_dir) + 1)
    # 单位由秒统一转为毫秒输出
    result = lib.analyse(sn, frame_mode.value, int(fps), start_index, end_index) * 1000.0
    logger.info(f'load_analyzer result:{result}ms')
    return result
