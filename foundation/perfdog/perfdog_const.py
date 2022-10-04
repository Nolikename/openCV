# ! /usr/local/bin
# -*- coding: utf-8 -*-
"""
@Time: 2022/3/7 下午3:53
@author: jacknli
@File: perfdog_const.py
@Desc: perfdog常量相关
"""
import os
import platform

TOKEN = "f828930ee90b4c8cb41371c94c1f21d59d8ea9ee95ab5ab6e0a4843e8b0ebb7b"
current_dir = os.path.dirname(os.path.abspath(__file__))

PLATFORM_MAC = "Darwin"
PLATFORM_LINUX = "Linux"
PLATFORM_WIN = "Windows"

PERFDOG_CONF = {
    PLATFORM_MAC: {
        "url": "https://perfdog.qq.com/account/download/service_mac",
        "executable_file_name": "PerfDogService",
        "download_name": "PerfDogService.tar.gz"
    },
    PLATFORM_LINUX: {
        "url": "https://perfdog.qq.com/account/download/service_linux",
        "executable_file_name": "PerfDogService",
        "download_name": "PerfDogService.tar.gz"
    },
    PLATFORM_WIN: {
        "url": "https://perfdog.qq.com/account/download/service_win",
        "executable_file_name": "PerfDogService.exe",
        "download_name": "PerfDogService.zip"
    },
}

# 根据电脑系统设置相应的PerfDog配置
sysstr = platform.system()
PLATFORM_CONF = PERFDOG_CONF[PLATFORM_MAC]
if sysstr == PLATFORM_LINUX:
    PLATFORM_CONF = PERFDOG_CONF[PLATFORM_LINUX]
elif sysstr == PLATFORM_WIN:
    PLATFORM_CONF = PERFDOG_CONF[PLATFORM_WIN]

# PerfDogService的文件夹路径, 若本地已下载过，则修改下路径
PERFDOG_SERVICE_DIR = os.path.join(current_dir, "PerfDogService")

PD_FPS = "fps"
PD_INTER_FRAME = "InterFrame"
PD_APP_USAGE = "AppUsage"
PD_TOTAL_USAGE = "TotalUsage"
PD_CPU_CLOCK = "CpuClock"
PD_MEMORY = "Memory"
PD_SWAP_MEMORY = "SwapMemory"
PD_CORE_USAGE = "CoreUsage"
PD_CPU_TEMPERATURE = "CpuTemperature"
PD_JANK = "Jank"
PD_BIG_JANK = "BigJank"
PD_DOWN_SPEED = "DownSpeed"
PD_UP_SPEED = "UpSpeed"
PD_RENDER = "Render"
PD_TILER = "Tiler"
PD_DEVICE = "Device"
PD_VIRTUAL_MEMORY = "VirtualMemory"
PD_NORMALIZED_APP_USAGE = "Normalized_AppUsage"
PD_NORMALIZED_TOTAL_USAGE = "Normalized_TotalUsage"
PD_NON_FRAGMENT_UTILIZATION = "NonFragmentUtilization"
PD_FRAGMENT_UTILIZATION = "FragmentUtilization"
PD_AVAILABLE_MEMORY = "AvailableMemory"
PD_GPU_CLOCK = "GpuClock"
PD_GFX = "Gfx"
PD_GL = "GL"
PD_BUS_READ = "BusRead"
PD_BUS_WRITE = "BusWrite"
PD_PIXEL_THROUGHPUT = "PixelThroughput"
PD_NATIVE_PSS = "NativePss"
PD_STUTTER = "Stutter"
