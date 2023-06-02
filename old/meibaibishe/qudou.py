import cv2  # 导入cv2库，用于图像处理

global img, point  # 定义全局变量img和point，用于存储图像和鼠标点击的点
global inpaintMask  # 定义全局变量inpaintMask，用于存储图像修复的遮罩
import numpy as np  # 导入numpy库，用于处理数组


# 手动祛痘函数，响应鼠标事件
def manual_acne(event, x, y, flags, param):
    global img, point  # 使用全局变量img和point
    img2 = img.copy()  # 创建原始图像的副本
    height, width, n = img.shape  # 获取图像的高度、宽度和通道数
    inpaintMask = np.zeros((height, width), dtype=np.uint8)  # 创建一个空白遮罩，与原始图像大小相同
    if event == cv2.EVENT_LBUTTONDOWN:  # 当鼠标左键按下时
        point = (x, y)  # 记录鼠标点击的点
        cv2.circle(img2, point, 15, (0, 255, 0), -1)  # 在img2上画一个绿色圆圈，半径为15
        cv2.circle(inpaintMask, point, 15, 255, -1)  # 在inpaintMask上画一个白色圆圈，半径为15
        cv2.imshow("image", img2)  # 显示img2
    elif event == cv2.EVENT_LBUTTONUP:  # 当鼠标左键松开时
        cv2.circle(img2, point, 15, (0, 255, 0), -1)  # 在img2上画一个绿色圆圈，半径为15
        cv2.circle(inpaintMask, point, 15, 255, -1)  # 在inpaintMask上画一个白色圆圈，半径为15
        cv2.imshow("inpaintMask", inpaintMask)  # 显示inpaintMask
        cv2.imshow("image", img2)  # 显示img2
        cv2.imshow("image0", img)  # 显示原始图像
        result = cv2.inpaint(img, inpaintMask, 100, cv2.INPAINT_TELEA)  # 使用cv2.inpaint()函数进行图像修复
        cv2.imshow("result", result)  # 显示修复后的图像


if __name__ == "__main__":
    global img  # 使用全局变量img
    img = cv2.imread("2.jpg")  # 读取图像文件
    cv2.namedWindow("image")  # 创建一个名为"image"的窗口
    cv2.setMouseCallback("image", manual_acne)  # 为"image"窗口设置鼠标回调函数manual_acne
    cv2.imshow("image", img)  # 显示图像
    cv2.waitKey()  # 等待键盘按键
    cv2.destroyAllWindows()  # 销
