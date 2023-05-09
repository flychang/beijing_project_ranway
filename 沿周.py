import cv2
import numpy as np
# from PIL import ImageFont, ImageDraw, Image
import math
import MouseMinWidth

mx = 0
my = 0
radius0 = 81
radius1 = 102
lcx = 124
lcy = 198
lcenter = (lcx, lcy)  # 左圆心
rcx = 1142
rcy = 198
rcenter = (rcx, rcy)  # 右圆心
# 读取图片文件
img = cv2.imread("mskover.png")
xiaoup = cv2.imread("maskup.png")
xiaoleft = cv2.imread("maskleft.png")
xiaodown=cv2.imread("maskdown.png")
xiaoright=cv2.imread("maskright.png")
# 获取图像尺寸
# height, width, channels = img.shape
img_copy = img.copy()  # 保存原始图片的副本
print(img.shape)
def get_cercle(cx, cy):
    angle_rad = math.atan2(cy - my, mx - cx)
    if angle_rad >= 0:
        angle_rad1 = angle_rad
    else:
        angle_rad1 = angle_rad + 2 * 3.1415926
    # 就用弧度算，不需要转角度
    y2 = int(cy - (radius1 * math.sin(angle_rad1)))
    x2 = int(cx + (radius1 * math.cos(angle_rad1)))
    y1 = int(cy - (radius0 * math.sin(angle_rad1)))
    x1 = int(cx + (radius0 * math.cos(angle_rad1)))
    return x1, y1, x2, y2


def get_mouse_pos(event, x, y, flags, param):
    global mx, my, img, y2, x2, y1, x1
    # 微调高度，注意y轴正方向
    trim_up = -5
    trim_upup = -10
  # 设置需要显示的字体
        # fontpath = "font/simsun.ttc"
        # font = ImageFont.truetype(fontpath, 32)
        # img_pil = Image.fromarray(img_draw)
        # draw = ImageDraw.Draw(img_pil)
        # # # 绘制文字信息
        # draw.text((100, 300), "Hello World", font=font, fill=(255, 255, 255))
        # draw.text((100, 350), "你好", font=font, fill=(255, 255, 255))
        # img = np.array(img_pil)
        # cv2.imshow("add_text", img)
     #大图坐标转小图
    if event == cv2.EVENT_MOUSEMOVE:

        mx, my = x, y

        img_draw = img_copy.copy()
        print("鼠标坐标：", (x, y))
        angle_rad = 0
        # 把左右圆心标注出来
        img_draw[lcy - 1:lcy + 1, lcx - 1:lcx + 1] = [255, 255, 255]
        img_draw[rcy - 1:rcy + 1, rcx - 1:rcx + 1] = [255, 255, 255]
        if lcx > mx >= 0:
            x1, y1, x2, y2 = get_cercle(lcx, lcy)
            # 大图坐标转小图坐标，调用亿力的函数
            flag, width = MouseMinWidth.MouseMinWidthInRing(x2 - 22, y2 - 96, x1 - 22, y1 - 96, xiaoleft)
        # 计算中间上部条形
        if lcx <= mx < rcx and 0 < my <= rcy:
            x1 = x2 = mx
            y1 = lcy - radius1
            y2 = lcy - radius0
            # 大图坐标转小图坐标，调用亿力的函数
            xx = x1 - lcx
            flag, width = MouseMinWidth.MouseMinWidthInLine(xx, xiaoup)
        # 计算中间下部条形
        if lcx <= mx < rcx and my > rcy:
            x1 = x2 = mx
            y1 = lcy + radius1
            y2 = lcy + radius0
            # 大图坐标转小图坐标，调用亿力的函数
            xx = x1 - lcx
            flag, width = MouseMinWidth.MouseMinWidthInLine(xx, xiaodown)
        # 计算右侧半圆弧度值
        if mx >= rcx:
            x1, y1, x2, y2 = get_cercle(rcx, rcy)
            # 大图坐标转小图坐标，调用亿力的函数
            flag, width = MouseMinWidth.MouseMinWidthInRing(x2 - 1142, y2 - 96, x1 - 1142, y1 - 96, xiaoright)