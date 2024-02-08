import streamlit as st
import datetime as datetime
import data
import function
import qianfan
import os
from pytz import timezone

os.environ["QIANFAN_AK"] = ""
os.environ["QIANFAN_SK"] = ""
chat_comp = qianfan.ChatCompletion()

#layout="wide",
st.set_page_config(page_title="周易大师", page_icon="☯️", initial_sidebar_state="expanded")

# 导入卦象列表
gua_list = data.gua_list
#导入图像对应表
image_dict = data.image_dict

def main():
   default_date = datetime.datetime.now().date()
   # 输入问题
   st.markdown("<h1 class='title' style='text-align: center;font-size: 25px'>周易大师</h1>", unsafe_allow_html=True)

   input_content = st.text_input("请输入您心中的疑问：")
   # 输入出生年月日
   col1, col2, col3,col4 = st.columns((1, 1, 1, 1))
   year = col1.selectbox("请输入出生年(公历)", range(1960, default_date.year+1), index = default_date.year - 1960)
   month = col2.selectbox("请输入出生月(公历)", range(1, 13), index = default_date.month - 1)
   day = col3.selectbox("请输入出生日(公历)", range(1, 32),index = default_date.day - 1)
   hour = col4.selectbox("请输入出生时(公历)", range(0, 24))
   # 输入数字
   col1, col2 = st.columns((1, 1))
   num_1 = col1.number_input("直觉输入上卦数字", step=1)
   num_2 = col2.number_input("直觉输入下卦数字", step=1)
   # 增加按钮
   if st.button("运行梅花易数起卦程序和八字立春切换算法"):
      if input_content:
         # 采用梅花易数+随机数起卦
         st.success("梅花易数+数字起卦，当前时间为：" + default_date.strftime("%Y-%m-%d %H:%M"))
         st.success(f"当前数字为:{num_1} {num_2}")
         gua, gua_result, gua_uncertain = function.QG(num_1,num_2)
         author=function.Lunar(year, month, day, hour)
         st.success(f"公历生日:{year}年{month}月{day}日{hour}时")
         st.success(f"农历生日:{author.lunarYear}年{author.lunarMonth}月{author.lunarDay}日")
         st.success(f"八字:{author.year8Char} {author.month8Char} {author.day8Char} {author.twohour8Char}")
         st.success(f"属相:{author.chineseYearZodiac}")
         st.success(f"星座:{author.starZodiac}")
         # 显示占卜结果
         # 在网页上显示带有变量的居中文本
         st.success(f"根据此问题所卜卦为：")
         function.Figure(gua_result)
         st.markdown(f"<p style='font-size: 20px; text-align:center'>{gua}</p>", unsafe_allow_html=True)
         function.Figure(gua_uncertain)
         # 发送给ChatGPT进行解释
         prompt = "请根据抽到的卦给出卦名和动爻的含义，结合属相、星座、八字和卦象一起解释卜卦的内容："
         content = f"属相是{author.chineseYearZodiac}，星座是{author.starZodiac}，八字是{author.year8Char} {author.month8Char} {author.day8Char} {author.twohour8Char}，需要卜卦的内容是{input_content}，抽到的卦是：{gua}"
         st.success("卦像：" + content)
         with st.spinner("解卦中..."):
            resp = chat_comp.do(model="ERNIE-Bot-4", messages=[{
               "role": "user",
               "content": "以学习的目的" + prompt + content
            }])
         st.balloons()
         st.info("解卦成功!")
         st.markdown(resp.body["result"])
         # 程序说明
         st.warning("本程序沿用先天八卦，结合梅花易数+数字起卦，并包含动爻分析，卜卦后由ChatGPT进行解卦。信则有，不信则无，请勿认真。")
      else:
         st.success("请在上方输入框写下您心中的疑问")
if __name__ == "__main__":
   main()