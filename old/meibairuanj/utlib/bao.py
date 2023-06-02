
# """
# 图像基础调整: 图像的亮度、对比度、色度，还可以用于增强图像的锐度,美白
# """

from PIL import Image
from PIL import ImageEnhance

def ColorEnhancement():
    # '''
    # #色度增强 : 饱和度  color=1,保持原图像不变
    # '''
    filepath = './static/images/1.jpg'
    color = 1.9
    image = Image.open(filepath)
    enh_col = ImageEnhance.Color(image)
    image_colored = enh_col.enhance(color)
    image_colored.save('./static/images/bao.jpg')


