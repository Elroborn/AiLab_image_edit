import suanpan
from suanpan.app import app
from suanpan.app.arguments import Folder,File,String
import os
import json
from glob import glob
import pandas as pd
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
colors = {'红色':(255,0,0),'绿色':(0,255,0),'蓝色':(0,0,255),'黑色':(0,0,0),'白色':(255,255,255)}
fonts = {'宋体':'msyh.ttc','黑体':'黑体.otf','圆体':'圆体.ttf'}
color = ""
font = 'msyh.ttc'
def text_edit(img_path,pt1,pt2,new_txt,font_color = (255,255,255),font_size = 35):
    """pt1，pt2是左上角和右下角"""

    img = cv2.imread(img_path)

    print(pt1)
    img = cv2ImgAddText(img,new_txt,pt1,font_color,font_size)


    cv2.imwrite("./res/"+new_txt+".jpg", img)




# 因为cv2不支持中文写文字
def cv2ImgAddText(img, text, pt1, font_color=(0, 255, 0), font_size=20):
    left,top = pt1[0],pt1[1]
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "font/%s"%font, font_size, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, font_color, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def main(image_path,csv_path,json_path):
    data = json.load(open(json_path,encoding='utf-8'))
    annot = data["metadata"]
    names = pd.read_csv(csv_path, header=None)


    for key in annot.keys():
        x, y, w, h = annot[key]['xy'][1:]
        for i in names[0]:  # 无列头 用0
            new_txt = i
            pt1 = (x,y)
            pt2 = (x+w,y+h)
            text_edit(image_path, pt1, pt2, new_txt, color)

@app.input(Folder(key="inputData1"))
@app.input(Folder(key="inputData2"))
@app.input(Folder(key="inputData3"))
@app.param(String(key="param1"))
@app.param(String(key="param2"))
@app.output(Folder(key="outputData1"))
def image_edit(context):
    args = context.args
    print("*"*20)
    print(args.inputData1)
    dir_name = args.inputData1
    global color
    color = colors[args.param1]
    print(color)
    global font
    font = fonts[args.param2]
    print(font)

    image_path = glob("%s/*.jpg"%args.inputData2)[0]
    csv_path = glob("%s/*.csv"%args.inputData3)[0]
    json_path = dir_name+"/project.json"
    main(image_path,csv_path,json_path)





    return "./res"


if __name__ == "__main__":
    suanpan.run(app)
