#!/bin/python
# 祛痘美白

import numpy as np  # 导入numpy库，用于处理数组
import cv2  # 导入cv2库，用于图像处理


# 磨皮函数
def mopi():
    '''
    Dest =(Src * (100 - Opacity) + (Src + 2 * GuassBlur(EPFFilter(Src) - Src + 128) - 256) * Opacity) /100 ;
    https://my.oschina.net/wujux/blog/1563461
    '''
    img = cv2.imread("./static/images/1.jpg")  # 读取图像文件
    dst = np.zeros_like(img)  # 创建一个与原始图像大小相同的空白图像
    v1 = 3  # 磨皮程度
    v2 = 1  # 细节程度
    dx = v1 * 5  # 双边滤波参数之一
    fc = v1 * 12.5  # 双边滤波参数之一
    p = 0.1  # 透明度参数

    temp4 = np.zeros_like(img)  # 创建一个与原始图像大小相同的空白图像
    temp1 = cv2.bilateralFilter(img, dx, fc, fc)  # 对原始图像进行双边滤波
    temp2 = cv2.subtract(temp1, img)  # 计算滤波后的图像与原始图像的差值
    temp2 = cv2.add(temp2, (10, 10, 10, 128))  # 将差值图像的像素值增加一个偏移量
    temp3 = cv2.GaussianBlur(temp2, (2 * v2 - 1, 2 * v2 - 1), 0)  # 对差值图像进行高斯模糊
    temp4 = cv2.add(img, temp3)  # 将模糊后的差值图像与原始图像相加
    dst = cv2.addWeighted(img, p, temp4, 1 - p, 0.0)  # 计算加权和，实现透明度混合
    dst = cv2.add(dst, (10, 10, 10, 255))  # 为输出图像增加一个偏移量
    cv2.imwrite('./static/images/mopi.jpg', dst)  # 保存磨皮后的图像
    fc = v1 * 12.5  # 双边滤波参数之一
    p = 0.1  # 透明度参数


# 去斑函数
def quban():
    '''
    Dest =(Src * (100 - Opacity) + (Src + 2 * GuassBlur(EPFFilter(Src) - Src + 128) - 256) * Opacity) /100 ;
    '''
    src = cv2.imread("./static/images/1.jpg")  # 读取图像文件
    dst = np.zeros_like(src)  # 创建一个与原始图像大小相同的空白图像
    v1 = 3  # 磨皮程度
    v2 = 1  # 细节程度
    dx = v1 * 5  # 双边滤波参数之一
    fc = v1 * 12.5  # 双边滤波参数之一
    p = 0.1  # 透明度参数
    temp4 = np.zeros_like(src)  # 创建一个与原始图像大小相同的空白图像
    temp1 = cv2.bilateralFilter(src, dx, fc, fc)  # 对原始图像进行双边滤波
    temp2 = cv2.subtract(temp1, src)  # 计算滤波后的图像与原始图像的差值
    temp2 = cv2.add(temp2, (10, 10, 10, 128))  # 将差值图像的像素值增加一个偏移量
    temp3 = cv2.GaussianBlur(temp2, (2 * v2 - 1, 2 * v2 - 1), 0)  # 对差值图像进行高斯模糊
    temp4 = cv2.subtract(cv2.add(cv2.add(temp3, temp3), src), (10, 10, 10, 255))  # 将模糊后的差值图像与原始图像相加，并减去一个偏移量

    dst = cv2.addWeighted(src, p, temp4, 1 - p, 0.0)  # 计算加权和，实现透明度混合
    dst = cv2.add(dst, (10, 10, 10, 255))  # 为输出图像增加一个偏移量
    cv2.imwrite('./static/images/quban.jpg', dst)  # 保存去斑后的图像
