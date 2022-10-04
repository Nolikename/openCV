from enum import Enum

# 最大分帧数
DEFAULT_MIN_FRAMES = 20
DEFAULT_MAX_FRAMES = 60


class MarkedStrategy(Enum):
    '''
    用于标识起始或者结束标记分别有多张图片时使用的策略。

    下面以起始标记输入多张标记图时为例说明
    AND：视频帧中同时存在多个标记图像即可满足要求
    OR： 视频帧中存在某一个标记图像即可满足要求
    '''
    AND = 1
    OR = 2


class DivideFrameMode(Enum):
    '''
    用于指定分帧使用opencv还是ffmpeg。

    FFMPEG：默认分帧策略,可以指定具体分帧数量，较为准确，计算量大
    OPENCV：分帧数量相对较少，快速
    '''
    OPENCV = 1
    FFMPEG = 2


class MarkedParams:
    def __init__(self):
        # 标记起点图片
        self.__start_marked_point_list = []
        # 多个启动图片查找策略
        self.__start_marked_strategy = None
        # 标记终点图片
        self.__end_marked_point_list = []
        # 多个终点图片查找策略
        self.__end_marked_strategy = None
        # 视频路径
        self.__video_path = ""
        # 图片上面是否有十字标记。（在开发者模式 -> 指针位置打开为True 强烈推荐打开）
        self.__point_position_marked = False
        # 默认True：计算起始标记图片第一次出现时位置，False：计算起始标记图片在视频中出现后第一次消失的位置
        self.__start_marked_use_appear = True
        # 默认True：计算终点标记图片第一次出现时位置，False：计算终点标记图片在视频中出现后第一次消失的位置
        self.__end_marked_use_appear = True
        # 视频分帧策略，默认opencv方式
        self.__divide_frame_mode = DivideFrameMode.FFMPEG
        # __frame_mode 为ffmpeg时 参数有效
        self.__divide_frame_fps = DEFAULT_MAX_FRAMES

    def set_video_path(self, video_path: str):
        '''
        设置分帧视频所在路径
        Args:
            video_path: 视频路径
        '''
        self.__video_path = video_path

    def add_start_marked_img_path(self, marked_img_path: str):
        '''
        标记起点图片，可多次调用设置多张图片
        如果设置多张图片需要调用set_start_marked_strategy设置策略。否则以第一张图片为准

        建议按照标记重要性顺序从高到底顺序依次添加标记(带十字标记图片放第一张)
        '''
        self.__start_marked_point_list.append(marked_img_path)

    def add_end_marked_img_path(self, marked_img_path: str):
        '''
        标记终点图片，可多次调用设置多张图片
        如果设置多张图片需要调用set_end_marked_strategy设置策略。否则以第一张图片为准
        '''
        self.__end_marked_point_list.append(marked_img_path)

    def set_start_marked_strategy(self, strategy: Enum):
        '''
        用于标识起始或者结束标记分别有多张图片时使用的策略。
        MarkedStrategy.AND：视频帧中同时存在多个标记图像即可满足要求
        MarkedStrategy.OR： 视频帧中存在某一个标记图像即可满足要求
        Args:
            strategy: AND或者OR可选
        '''
        self.__start_marked_strategy = strategy

    def set_end_marked_strategy(self, strategy: Enum):
        '''
        用于标识起始或者结束标记分别有多张图片时使用的策略。
        MarkedStrategy.AND：视频帧中同时存在多个标记图像即可满足要求
        MarkedStrategy.OR： 视频帧中存在某一个标记图像即可满足要求
        Args:
            strategy: AND或者OR可选
        '''
        self.__end_marked_strategy = strategy

    def set_divide_frame_mode(self, divide_frame_mode: Enum, fps: int = 60):
        '''
         用于指定分帧使用opencv还是ffmpeg。

            FFMPEG：默认使用ffmpeg进行视频分帧，可以指定具体分帧数量，较为准确，计算量大
            OPENCV：使用opencv分帧策略，分帧数量相对较少，快速
        Args:
            divide_frame_mode: DivideFrameMode.OPENCV或者DivideFrameMode.FFMPEG
            fps: 使用DivideFrameMode.FFMPEG时,设置参数有效。取值范围[20，60]
        '''
        self.__divide_frame_mode = divide_frame_mode
        if fps < DEFAULT_MIN_FRAMES:
            fps = DEFAULT_MIN_FRAMES
        if fps > DEFAULT_MAX_FRAMES:
            fps = DEFAULT_MAX_FRAMES
        self.__divide_frame_fps = fps

    def get_divide_frame_mode(self):
        return self.__divide_frame_mode

    def get_divide_frame_fps(self):
        return self.__divide_frame_fps

    def set_point_position_marked(self, point_position_marked: bool):
        '''
        默认True：
        True:标记图片上面有十字标记。（ 在【开发者模式】-> 【指针位置】打开为True 强烈推荐打开）
        False:标记图片上没有十字标记
        '''
        self.__point_position_marked = point_position_marked

    def set_start_marked_use_appear(self, appear: bool = True):
        '''
        默认True：
        True: 计算起始标记图片第一次出现时位置<p>
        False：计算起始标记图片在视频中出现后第一次消失的位置
        '''
        self.__start_marked_use_appear = appear

    def set_end_marked_use_appear(self, appear: bool = True):
        '''
        默认True：
        True: 计算结束标记图片第一次出现时位置<p>
        False：计算结束标记图片在视频中出现后第一次消失的位置
        '''
        self.__end_marked_use_appear = appear

    def add_start_marked_img_path_list(self, marked_img_path_list: list):
        '''
        标记起点图片
        如果设置多张图片需要调用set_start_marked_strategy设置策略。否则以第一张图片为准
        '''
        self.__start_marked_point_list.extend(marked_img_path_list)

    def add_end_marked_img_path_list(self, marked_img_path_list: list):
        '''
        标记终点图片
        如果设置多张图片需要调用set_end_marked_strategy设置策略。否则以第一张图片为准
        '''
        self.__end_marked_point_list.extend(marked_img_path_list)

    def get_start_marked_img_path_list(self):
        return self.__start_marked_point_list

    def get_end_marked_img_path_list(self):
        return self.__end_marked_point_list

    def get_video_path(self):
        return self.__video_path

    def get_start_marked_strategy(self):
        return self.__start_marked_strategy

    def get_end_marked_strategy(self):
        return self.__end_marked_strategy

    def is_start_marked_appear(self):
        return self.__start_marked_use_appear

    def is_end_marked_use_appear(self):
        return self.__end_marked_use_appear

    def is_point_position_marked(self):
        return self.__point_position_marked


class MarkedResult:

    def __init__(self, status, fail_msg):
        # 执行状态 True时后续字段才有意义
        self.status = status
        # 执行状态为Fail时具体原因
        self.fail_msg = fail_msg
        # 标记起点图片第一帧位置（内容为该帧对应时间）
        self.__first_frame_index_list = []
        # 标记终点图片第一帧位置（内容为该帧对应时间）
        self.__last_frame_index_list = []
        # 起始帧在所有帧中位置
        self.__start_marked_pos = 0
        # 结束帧在所有帧中位置
        self.__end_marked_pos = 0

    def update_status(self, status, fail_msg):
        self.status = status
        self.fail_msg = fail_msg

    def get_first_frame_index_list(self):
        return self.__first_frame_index_list

    def get_last_frame_index_list(self):
        return self.__last_frame_index_list

    def set_start_marked_pos(self, start_pos: int):
        self.__start_marked_pos = start_pos

    def get_start_marked_pos(self):
        return self.__start_marked_pos

    def set_end_marked_pos(self, end_pos: int):
        self.__end_marked_pos = end_pos

    def get_end_marked_pos(self):
        return self.__end_marked_pos
