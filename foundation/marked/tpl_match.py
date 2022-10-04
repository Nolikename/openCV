# version: 2.2
from threading import Thread
import cv2 as cv
import numpy as np
from loguru import logger

class RThread(Thread):
    def __init__(self, target, args):
        super(RThread, self).__init__()
        self.func = target
        self.args = args
        self.result = None

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        return self.result


def match_thread(tpl, img, ratio, scale_type, tpl_pos=None, tpl_l=None, offset=None, pos_weight=0.05):
    img_sp = img.shape
    tpl_sp = tpl.shape
    if tpl_sp[0] > img_sp[0] or tpl_sp[1] > img_sp[1]:
        return None
    if tpl_l is not None:
        tpll_sp = tpl_l.shape
        if tpll_sp[0] > img_sp[0] or tpll_sp[1] > img_sp[1]:
            tpl_l = None

    # img_blur = cv.medianBlur(img, 3)  # cv.GaussianBlur(img_re, (3, 3), 0)
    # tpl_blur = cv.medianBlur(tpl, 3)  # cv.GaussianBlur(tpl, (3, 3), 0)

    res_s = cv.matchTemplate(tpl, img, cv.TM_CCOEFF_NORMED)
    if tpl_l is not None:
        res_l = cv.matchTemplate(tpl_l, img, cv.TM_CCOEFF_NORMED)

        warp_matrix = np.float32([[1, 0, offset[0]], [0, 1, offset[1]]])
        sp_l = res_l.shape
        res_l = cv.warpAffine(res_l, warp_matrix, (sp_l[1], sp_l[0]))
        sp_s = res_s.shape
        res_l = cv.copyMakeBorder(res_l, 0, sp_s[0] - sp_l[0], 0, sp_s[1] - sp_l[1], cv.BORDER_CONSTANT, value=(0))
        res = res_s + res_l * 0.8
        # res = res_l
        # min_vals, max_vals, min_locs, max_locs = cv.minMaxLoc(res_s)
        # min_vall, max_vall, min_locl, max_locl = cv.minMaxLoc(res_l)
    else:
        res = res_s

    pos_ratio = 1
    if scale_type == "img":
        pos_ratio = ratio

    if tpl_pos:
        # flat_indices = np.argsort(-res.ravel())
        # row_indices, col_indices = np.unravel_index(flat_indices, res.shape)
        flat_indices = np.argpartition(-res.ravel(), 10)[:11]
        row_indices, col_indices = np.unravel_index(flat_indices, res.shape)
        rlt = []
        for i in range(10):
            r = row_indices[i]
            c = col_indices[i]
            distance = ((r - tpl_pos[1] * pos_ratio) ** 2 + (c - tpl_pos[0] * pos_ratio) ** 2) ** 0.5
            # sim：相似度 = 图像相似度 + 坐标权重/（坐标距离/100 + 1）
            sim = res[r][c] + pos_weight / (distance / 100 + 1)
            # sim：相似度  (c, r)：左上角坐标
            rlt.append([sim, (c, r)])

        # def get_dist(item):
        #     return item[0]
        #
        # rlt.sort(key=get_dist, reverse=True)
        # 按照相似度从高到低排序
        rlt.sort(reverse=True)
        # 取第0位，即相似度最高的值
        max_val = rlt[0][0]
        max_loc = rlt[0][1]
        return [max_val, max_loc, ratio, scale_type, rlt]

    _, max_val, _, max_loc = cv.minMaxLoc(res)
    return [max_val, max_loc, ratio, scale_type, []]


def translucent_proc(img, binary_thr):
    img_blur = cv.GaussianBlur(img, (3, 3), 0)
    img_gray = cv.cvtColor(img_blur, cv.COLOR_BGR2GRAY)
    _, img_binary = cv.threshold(img_gray, binary_thr, 255, cv.THRESH_BINARY)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
    img_proc = cv.erode(img_binary, kernel)
    return img_proc


def tpl_match(tpl, img, tpl_pos=None, pos_weight=0.05, scare_size=20, scare_step=1, is_translucent=False, tpl_l=None,
              offset=None):
    if is_translucent:
        img_blur = cv.GaussianBlur(tpl, (3, 3), 0)
        binary_thr = np.mean(img_blur)
        tpl = translucent_proc(tpl, binary_thr)
        img = translucent_proc(img, binary_thr)
        if tpl_l is not None:
            tpl_l = translucent_proc(tpl_l, binary_thr)

    img_sp = img.shape
    tpl_sp = tpl.shape
    if tpl_l is not None:
        tpll_sp = tpl_l.shape
    t_list = []
    isp_re = (0, 0)
    tsp_re = (0, 0)

    for ratio in range(1, scare_size, scare_step):
        ratio = 1 - ratio / 100
        if 0.7 < ratio < 0.95:
            continue
        
        sps_re = (round(tpl_sp[1] * ratio), round(tpl_sp[0] * ratio))
        if sps_re != tsp_re:
            tpl_re = cv.resize(tpl, sps_re)
            if tpl_l is not None:
                spl_re = (round(tpll_sp[1] * ratio), round(tpll_sp[0] * ratio))
                tpll_re = cv.resize(tpl_l, spl_re)
                offset_re = [round(offset[0] * ratio), round(offset[1] * ratio)]
            else:
                tpll_re = tpl_l
                offset_re = offset

            t = RThread(target=match_thread,
                        args=(tpl_re, img, ratio, "tpl", tpl_pos, tpll_re, offset_re, pos_weight))
            t.start()
            t_list.append(t)
            tsp_re = sps_re

    t = RThread(target=match_thread, args=(tpl, img, 1, "none", tpl_pos, tpl_l, offset, pos_weight))
    t.start()
    t_list.append(t)

    thread_rlt = []
    for t in t_list:
        t.join()
        result = t.get_result()
        if result:
            thread_rlt.append(result)

    thread_rlt.sort(reverse=True)
    # max_val：相似度  max_loc：左上角坐标   ratio：比率
    # scale_type:缩放类型（img:目标图缩放，tpl:原控件图缩放，None:不缩放） res_s：最优一次查找中所有结果
    max_val, max_loc, ratio, scale_type, res_s = thread_rlt[0]
    logger.debug(f"模版匹配执行完毕：最高相似度 {max_val} 位置 {max_loc} 缩放类型 {scale_type} 缩放比例 {ratio}")
    target_center = trans_loc(max_loc, ratio, scale_type, tpl_sp)

    # max_val：相似度  target_center：中心点和左上角顶点
    return max_val, target_center, ratio, scale_type, res_s


def trans_loc(loc, ratio, scale_type, tpl_sp):
    """获取中心点和左上角顶点.

    Args:
        loc : 左上角坐标
        ratio : 比率
        scale_type : 缩放类型
        tpl_sp : 原图shape

    Returns:
        loc: 中心点和左上角顶点
    """
    if scale_type == "img":
        loc = (round(loc[0] / ratio), round(loc[1] / ratio))
    width = tpl_sp[1]
    height = tpl_sp[0]
    if scale_type == "img":
        width /= ratio
        height /= ratio
    elif scale_type == "tpl":
        width *= ratio
        height *= ratio
    # 中心点和左上角顶点
    loc = (loc[0] + int(width / 2), loc[1] + int(height / 2), loc[0], loc[1])
    return loc
