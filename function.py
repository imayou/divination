import streamlit as st
import datetime
import data
import cnlunar
from PIL import Image

# 导入卦象列表
gua_list = data.gua_list
#导入图像对应表
image_dict = data.image_dict

# 起卦程序
def QG(num1,num2):
    # 获取当前时间
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    # 计算余数
    up=(year+month+day+num1)%8
    down=(year+month+day+hour+num2)%8
    uncertain=(year+month+day+hour+num1+num2)%6
    # 确定上下卦及动爻
    up_result=switch_up_down(up)
    down_result=switch_up_down(down)
    uncertain_result=switch_uncertain(uncertain)
    # 获取上下卦二进制编码
    up_gua=switch_up_down_gua(up)
    down_gua=switch_up_down_gua(down)
    gua_result=up_gua+down_gua
    # 寻找对应的卦名和序号
    gua_name = ''
    gua_num =0
    for a in gua_list:
        if a['gua'] == gua_result:
            gua_name = a['name']
            gua_num = a['num']
            break
    # 判断动爻情况
    gua_chars = list(gua_result)
    c = gua_chars[uncertain] 
    if c == "1":
        result = "0"
    elif c == "0":
        result = "1"
    gua_chars[uncertain] = result
    gua_uncertain = ''
    for c in gua_chars:
        gua_uncertain += c
    gua_uncertain_name = ''
    gua_uncertain_num = 0
    for a in gua_list:
        if a['gua'] == gua_uncertain:
            gua_uncertain_name = a['name']
            gua_uncertain_num = a['num']
            break
    # 返回结果
    result = f"上卦为{up_result}，下卦为{down_result}，动爻为{uncertain_result}，卦名为{gua_name}，第{gua_num}卦，根据动爻，此卦还可能变为第{gua_uncertain_num}卦，卦名为{gua_uncertain_name}"
    return result,gua_result,gua_uncertain

# 上卦及下卦
def switch_up_down(value):
    switcher = {
        0: "坤",
        1: "乾",
        2: "兑",
        3: "离",
        4: "震",
        5: "巽",
        6: "坎",
        7: "艮",
        "default": "error"
    }
    return switcher.get(value, "default")

# 上卦及下卦所对应二进制编码
def switch_up_down_gua(value):
    switcher = {
        0: "000",
        1: "111",
        2: "011",
        3: "101",
        4: "001",
        5: "110",
        6: "010",
        7: "100",
        "default": "error"
    }
    return switcher.get(value, "default")

# 动爻
def switch_uncertain(value):
    switcher = {
        0: "上爻",
        1: "初爻",
        2: "二爻",
        3: "三爻",
        4: "四爻",
        5: "五爻",
        "default": "error"
    }
    return switcher.get(value, "default")

# 卦象图案显示
def Figure(gua):
    gua_chars = list(gua)
    for char in gua_chars:
        image_file = image_dict[char]
        image = Image.open(image_file)
        col1, col2, col3 = st.columns((1, 1, 1))
        col1.write("")
        col2.image(image, width=150,use_column_width=True)
        col3.write("")

# 八字立春切换算法
def Lunar(year, month, day, hour):
    year = int(year)
    month = int(month)
    day = int(day)
    hour = int(hour)
    a = cnlunar.Lunar(datetime.datetime(year, month, day, hour), godType='8char', year8Char='beginningOfSpring')
    return a