import os
import collections
import cv2
import numpy as np

from loguru import logger
from foundation.marked.marked_params import MarkedParams
from foundation.marked.marked_params import MarkedStrategy
from foundation.marked.marked_params import MarkedResult
from foundation.marked.tpl_match import tpl_match

RGBA_CHANNELS = 4
RGB_CHANNELS = 3
# 标记相似度阈值
CV_THRESHOLD = 0.85
# 用于CV时图片缩放 SCARE_SIZE=30 表示最大30%的缩放，SCARE_STEP=3 每次缩放步长为3%
SCARE_SIZE = 40
SCARE_STEP = 3
# 参数校验返回类
CHECK_RESULT = collections.namedtuple('CheckResult', ['ok', 'fail_msg'])
CALC_RESULT = collections.namedtuple('CalcResult', ['status', 'fail_msg', 'frame_index'])


# 图像读取
def __get_img_data(image_path):
    return cv2.imread(image_path)


def __check_file_name(name: str) -> bool:
    # 必须是 png/jpg 后缀
    suffix = name[-4:]
    if suffix != '.png' and suffix != '.jpg':
        return False
    # 文件名必须是全数字
    try:
        int(name[:-4])
        return True
    except ValueError as e:
        return False


def __get_file_list(path: str):
    if not os.path.exists(path):
        logger.info(f"视频帧目录不存在：{path}")
        return None
    for path, dir_list, file_list in os.walk(path):
        # 列表中过滤掉不合法的文件名文件
        file_list = list(filter(__check_file_name, file_list))
        # 拿到文件列表后，要根据文件名中的数字进行排序
        file_list.sort(key=lambda x: int(x[:-4]))
        logger.info(f"一共 {len(file_list)} 个视频帧画面")
        return file_list
    logger.info(f"没有找到视频帧画面：{path}")
    return None


def __file_idx_to_frame_idx(file_list, file_idx: int):
    # -4 是为了去掉文件名后缀 ".png"
    frame = file_list[file_idx][:-4]
    logger.info(f'_file_idx_to_frame_idx：{file_idx} >> {frame}')
    return int(frame)


def __run_search(target_img_path: str, start_index: int, file_list, frames_dir: str,
                 mark_params: MarkedParams, is_start: bool, and_strategy: bool = False,
                 img_index: int = 0):
    """
        常规遍历查找
        Args:
            target_img_path: 待查找的目标图像及其匹配模式
            start_index: 查找范围的起始索引值，即从哪张图片开始做抽样查找
            file_list: 图片目录的文件列表
            frames_dir: 存储手机录屏分帧图片的目录
            mark_params: 标记参数
            is_start: 是否起始标记
            and_strategy: 是否为and策略模式（）
        Returns: 找到的位置，未找到则返回 -1
        """
    total = len(file_list)
    max_val = 0.0
    match_first = False
    max_val_index = 0
    for cur_frame_index in range(start_index, total):
        target_img = __get_img_data(target_img_path)
        current_img = __get_img_data(os.path.join(frames_dir, file_list[cur_frame_index]))
        val, center, _, _, _ = tpl_match(target_img, current_img, scare_size=SCARE_SIZE, scare_step=SCARE_STEP)
        # 起始标记点后续可能多张图片满足要求,必定连续，取相似度最高的那个
        if val > CV_THRESHOLD:
            match_first = True
            if max_val < val:
                max_val = val
                max_val_index = cur_frame_index
            # 图像没有触摸点标记或者结束图标记返回第一次满足要求的即可
            if is_start:
                # 开始标记
                if mark_params.is_start_marked_appear():
                    # 1)图片上面没有十字标记（第一张标记图）  2)and模式，第二张标记及其以后出现的图片(无附近最大相似度逻辑，立即返回)
                    if not mark_params.is_point_position_marked() or (and_strategy and img_index > 0):
                        return cur_frame_index
            else:
                # 结束标记，只要是匹配第一次出现都走这个逻辑
                if mark_params.is_end_marked_use_appear():
                    return cur_frame_index
            # 页面跳转后仍然存在标识节点导致全程大于目标阈值
            if cur_frame_index + 1 == total:
                return max_val_index
        else:
            if is_start:
                # 开始标记
                if mark_params.is_start_marked_appear():  # 匹配第一次出现
                    if match_first:
                        # 第一次出现位置附近拥有最大相似度的索引
                        return max_val_index
                else:
                    #  匹配第一次消失
                    # 1）第一次出现后消失的标记图片（第一张标记图）
                    # 2）and模式，第二张标记及其以后消失的图片，立即返回
                    if match_first or (and_strategy and img_index > 0):
                        return cur_frame_index
            else:
                # 结束标记：只要是匹配第一次消失都走这个逻辑
                if not mark_params.is_end_marked_use_appear():
                    if match_first or (and_strategy and img_index > 0):
                        # 结束标记，出现后第一次消失时的索引
                        return cur_frame_index
    return -1


# 检测必要输入参数是否存在
def check_marked_params(mark_params: MarkedParams) -> CHECK_RESULT:
    # 检查输入是否存在
    if not mark_params.get_start_marked_img_path_list() \
            and not mark_params.get_end_marked_img_path_list():
        return CHECK_RESULT(False, '标识图片不存在')
    if not mark_params.get_video_path() or not os.path.exists(mark_params.get_video_path()):
        return CHECK_RESULT(False, '视频文件不存在')
    return CHECK_RESULT(True, '')


def __calc_start_mark(mark_params: MarkedParams, default_frames_dir: str, file_list: []) -> CALC_RESULT:
    '''
    计算起点标记逻辑
    Args:
        mark_params: 标记参数
        default_frames_dir:默认帧所在文件夹路径
        file_list:帧文件名列表

    Returns:
        返回值1：计算标记执行状态 True:正常，False：异常状态
        返回值2：失败后返回失败原因
        返回值3：标记帧位置索引
    '''
    if not mark_params.get_start_marked_img_path_list():
        # 无起始标记不需计算直接返回
        return CALC_RESULT(True, "", -1)
    if len(mark_params.get_start_marked_img_path_list()) == 1:
        # 单个标记元素 不需要设置策略
        start_frame_index = __run_search(target_img_path=mark_params.get_start_marked_img_path_list()[0],
                                         start_index=0,
                                         file_list=file_list,
                                         frames_dir=default_frames_dir,
                                         mark_params=mark_params,
                                         is_start=True)
        result_state = False if start_frame_index == -1 else True
        return CALC_RESULT(result_state, "", start_frame_index)
    # marked_num >1 多个标记元素 必须指定策略
    if not mark_params.get_start_marked_strategy():
        return CALC_RESULT(False, "多个标记元素起点计算,需要指定起点计算策略 set_start_marked_strategy", -1)
    elif mark_params.get_start_marked_strategy() == MarkedStrategy.OR:
        for index in range(len(mark_params.get_start_marked_img_path_list())):
            start_frame_index = __run_search(target_img_path=mark_params.get_start_marked_img_path_list()[index],
                                             start_index=0,
                                             file_list=file_list,
                                             frames_dir=default_frames_dir,
                                             mark_params=mark_params,
                                             is_start=True)
            if start_frame_index == -1:
                # 未找到继续找下一个
                continue
            logger.info(f'mark start | MarkedStrategy.OR | 第{index + 1}个标记被发现,'
                        f'在{__file_idx_to_frame_idx(file_list, start_frame_index)}帧')
            return CALC_RESULT(True, "", start_frame_index)
    elif mark_params.get_start_marked_strategy() == MarkedStrategy.AND:
        # 多个标记元素权重依次降低，查找会从上一个找到的帧依次往下查找,提高效率
        start_index = 0
        for index in range(len(mark_params.get_start_marked_img_path_list())):
            start_frame_index = __run_search(target_img_path=mark_params.get_start_marked_img_path_list()[index],
                                             start_index=start_index,
                                             file_list=file_list,
                                             frames_dir=default_frames_dir,
                                             mark_params=mark_params,
                                             is_start=True,
                                             and_strategy=True,
                                             img_index=index)
            if start_frame_index == -1:
                # 未找到终止查找
                return CALC_RESULT(False, f'mark start ｜ 第{index + 1}个标记未被发现', -1)
            start_index = start_frame_index
            logger.info(f'mark start | MarkedStrategy.AND ｜ 第{index + 1}个标记被发现,'
                        f'在{__file_idx_to_frame_idx(file_list, start_frame_index)}帧')
        # 确认最终的起始帧位置
        return CALC_RESULT(True, "", start_index)
    return CALC_RESULT(False, "标记未被发现", -1)


def __calc_end_mark(mark_params: MarkedParams, default_frames_dir: str, file_list: [],
                    start_frame_index: int) -> CALC_RESULT:
    '''
        计算结束标记逻辑
        Args:
            mark_params: 标记参数
            default_frames_dir:默认帧所在文件夹路径
            file_list:帧文件名列表

        Returns:
            返回值1：计算标记执行状态 True:正常，False：异常状态
            返回值2：失败后返回失败原因
            返回值3：标记帧位置索引

        '''
    if not mark_params.get_end_marked_img_path_list():
        # 无结束标记不需计算直接返回
        return CALC_RESULT(True, "", -1)
    start_index = start_frame_index + 1
    if len(mark_params.get_end_marked_img_path_list()) == 1:
        # 单个标记元素
        end_frame_index = __run_search(target_img_path=mark_params.get_end_marked_img_path_list()[0],
                                       start_index=start_index,
                                       file_list=file_list,
                                       frames_dir=default_frames_dir,
                                       mark_params=mark_params,
                                       is_start=False)
        result_state = False if end_frame_index == -1 else True
        return CALC_RESULT(result_state, "", end_frame_index)
    # marked_num >1 多个标记元素 必须指定策略
    if not mark_params.get_end_marked_strategy():
        return CALC_RESULT(False, "多个标记元素终点计算,需要指定终点计算策略 set_end_marked_strategy", -1)
    elif mark_params.get_end_marked_strategy() == MarkedStrategy.OR:
        for index in range(len(mark_params.get_end_marked_img_path_list())):
            end_frame_index = __run_search(target_img_path=mark_params.get_end_marked_img_path_list()[index],
                                           start_index=start_index,
                                           file_list=file_list,
                                           frames_dir=default_frames_dir,
                                           mark_params=mark_params,
                                           is_start=False)
            if end_frame_index == -1:
                # 未找到继续找下一个
                continue
            logger.info(f'mark end | MarkedStrategy.OR | 第{index + 1}个标记被发现,'
                        f'在{__file_idx_to_frame_idx(file_list, end_frame_index)}帧')
            return CALC_RESULT(True, "", end_frame_index)
    elif mark_params.get_end_marked_strategy() == MarkedStrategy.AND:
        # 多个标记元素权重依次降低，查找会从上一个找到的帧依次往下查找,提高效率
        for index in range(len(mark_params.get_end_marked_img_path_list())):
            # 单个标记元素
            end_frame_index = __run_search(target_img_path=mark_params.get_end_marked_img_path_list()[index],
                                           start_index=start_index,
                                           file_list=file_list,
                                           frames_dir=default_frames_dir,
                                           mark_params=mark_params,
                                           is_start=False,
                                           and_strategy=True,
                                           img_index=index)
            if end_frame_index == -1:
                # 未找到终止查找
                return CALC_RESULT(False, f'mark end ｜ 第{index + 1}个标记未被发现', -1)
            start_index = end_frame_index
            logger.info(f'mark end | MarkedStrategy.AND ｜ 第{index + 1}个标记被发现,'
                        f'在{__file_idx_to_frame_idx(file_list, end_frame_index)}帧')
        # 确认最终结束帧位置
        return CALC_RESULT(True, "", start_index)
    return CALC_RESULT(False, "标记未被发现", -1)


# 通过标记起始点和结束点图片确定耗时
def get_marked_img_position(mark_params: MarkedParams, default_frames_dir: str) -> MarkedResult:
    """
        输入开始和结束标记图片获取执行耗时
        Args:
            mark_params: 起始标记截图路径
            default_frames_dir: 视频所在目录文件夹
            fps: 视频帧率
        Returns:
            MarkedResult: 执行结果对象
    """
    # 检查输入是否存在
    check_result = check_marked_params(mark_params)
    if not check_result.ok:
        return MarkedResult(False, check_result.fail_msg)
    file_list = __get_file_list(default_frames_dir)
    if not file_list:
        return MarkedResult(False, "获取视频帧失败")
    marked_result = MarkedResult(True, "")

    # 计算起始帧位置
    start_cale_result = __calc_start_mark(mark_params, default_frames_dir, file_list)
    if not start_cale_result.status:
        marked_result.update_status(False, start_cale_result.fail_msg)
        return marked_result
    frame_index = __file_idx_to_frame_idx(file_list,
                                          start_cale_result.frame_index) if start_cale_result.frame_index >= 0 else -1
    marked_result.get_first_frame_index_list().append(frame_index)
    marked_result.set_start_marked_pos(start_cale_result.frame_index)

    # 计算结束帧位置
    end_cale_result = __calc_end_mark(mark_params, default_frames_dir, file_list, start_cale_result.frame_index)
    if not end_cale_result.status:
        marked_result.update_status(False, end_cale_result.fail_msg)
        return marked_result
    frame_index = __file_idx_to_frame_idx(file_list,
                                          end_cale_result.frame_index) if end_cale_result.frame_index > 0 else -1
    marked_result.get_last_frame_index_list().append(frame_index)
    marked_result.set_end_marked_pos(end_cale_result.frame_index)

    logger.info(f"\n起始帧文件编号：{marked_result.get_first_frame_index_list()}"
                f"\n结束帧文件编号：{marked_result.get_last_frame_index_list()}")
    return marked_result
