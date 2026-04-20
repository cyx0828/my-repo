from os import system

import streamlit as st
import os
from openai import OpenAI

st.set_page_config(
    page_title="AI Partner",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

#大标题
st.title("AI Partner")

#lOGO
st.logo("resources/mowan.jpg")

#系统提示词
system_prompt = "你是一个可爱美少女，你叫吴泽佑，请用充满少女心的语气回复问题"

#初始化聊天信息
if 'message' not in st.session_state:
    st.session_state.message = [ ]

#展示聊天信息
for message in st.session_state.message:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
#创造与ai大模型交互的客户端对象
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

#消息输入框
prompt = st.chat_input("请输入你的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("--------> 调用ai大模型，提示词：",prompt)
    st.session_state.message.append({"role": "user", "content": prompt})

    # 调用ai大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    print("<-------- 大模型返回结果，",response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)