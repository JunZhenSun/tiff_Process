import cv2
import matplotlib.pyplot as plt
import numpy as np
from numba import jit


def image_pre(x, min, max):  # 特异值剔除
    if x > max:
        return max
    if x < min:
        return min
    else:
        return x


@jit(nopython=True)  # 使用C++加快运行速度
def opti(img):  # 设置透明背景
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j, 0] == 0 and img[i, j, 1] == 0 and img[i, j, 2] == 0:
                img[i, j, 3] = 1.0
    return img


def read_tif(imgpath):  # 主函数 “三通道tiff”转“彩色png”
    img = cv2.imread(imgpath, 3)  # 读取图片 imgpath为图片所在位置
    print(img.dtype)

    fun1 = np.frompyfunc(image_pre, 3, 1)
    print("哈哈哈")
    img = fun1(img, 0, 1450).astype(np.uint16)

    min1 = img.min()
    max1 = 1450
    img = (img - min1) / (max1 - min1)
    img = img * 255
    img = img.astype(np.uint8)
    im_shape = img.shape
    print(im_shape)  # 显示图片大小和通道数  通道数为3
    b = img[:, :, 2]  # 蓝通道
    g = img[:, :, 1]  # 绿通道
    r = img[:, :, 0]  # 红通道



    # 通道拼接  两种方法
    bgr = cv2.merge([b, g, r])

    rgba = cv2.cvtColor(bgr, cv2.COLOR_RGB2RGBA)
    print(type(rgba))
    print(im_shape[0])
    # 背景设为透明
    opti(rgba)

    plt.matshow(rgba)  # matplotlib的matshow()可以直接看矩阵而不用进行位数转换
    cv2.imwrite("C:/Users/dell/Desktop/1.png", rgba)  # 保存图片


read_tif("D:/data/ndvi/Image20200510.tif")
