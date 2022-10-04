
# -*- coding: utf-8 -*-
"""
@Time: 2022/7/4 3:51 下午
@author: jacknli
@File: testCV.py
@Desc: 
"""

from foundation.marked.marked_params import MarkedStrategy


if __name__ == '__main__':
    from foundation.cv.cv_calculate import cv_analyse
    from foundation.marked.marked_params import MarkedParams, DivideFrameMode

    params = MarkedParams()
    params.set_divide_frame_mode(DivideFrameMode.FFMPEG, fps=25)
    params.set_start_marked_use_appear(False)
    params.set_end_marked_use_appear(True)
    params.set_end_marked_strategy(MarkedStrategy.OR)

    params.add_start_marked_img_path("/Users/geraltw/Desktop/start.png")
    params.add_end_marked_img_path("/Users/geraltw/Desktop/end.png")

    result = cv_analyse("/Users/geraltw/Desktop/abc/abc.mov", params)

