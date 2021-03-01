import cv2
import numpy as np


def read_tif(imgPath):  # 主函数 “三通道tiff”转“彩色png”
    img = cv2.imread(imgPath, 3)  # 读取图片 imgpath为图片所在位置
    # print(img.dtype)

    # 特异值剔除
    img[img > 1450] = 1450
    img[img < 0] = 0

    min1 = img.min()
    max1 = 1450
    img = ((img - min1) / (max1 - min1) * 255).astype(np.uint8)
    im_shape = img.shape
    print(im_shape)  # 显示图片大小和通道数  通道数为3
    b = img[:, :, 2]  # 蓝通道
    g = img[:, :, 1]  # 绿通道
    r = img[:, :, 0]  # 红通道

    x = r + b + g
    a = ((1 - np.equal(x, 0)) * 255).astype(np.uint8)

    # 通道拼接  两种方法
    rgba = cv2.merge([b, g, r, a])

    # plt.matshow(rgba)  # matplotlib的matshow()可以直接看矩阵而不用进行位数转换
    cv2.imwrite("C:/Users/dell/Desktop/1.png", rgba)  # 保存图片


read_tif(r"D:\data\007_anji\img2018-05.tif")
