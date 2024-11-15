# ################################
# Chat을 활용한 예시
# ################################

########## 구성 값 ##########
model = "gpt-4o"
title = "반말 친구 챗봇"
messages_base = [
    {
      "role": "system",
      "content": [{
          "type": "text",
          "text": "당신은 반말로 대화하는 나의 친근한 친구입니다."
      }]
    },
    {
      "role": "user",
      "content": [{
          "type": "text",
          "text": "안녕?"
      }]
    },
    {
      "role": "assistant",
      "content": [{
          "type": "text",
          "text": "안녕! 잘 지내지?"
      }]
    },
]

params = {
    "temperature":0,
    "max_tokens":2048,
    "top_p":1,
    "frequency_penalty":0,
    "presence_penalty":0,
    "response_format":{
      "type": "text"
    },
}



##############################################################################################
from openai import OpenAI
import streamlit as st

st.title(title)

client = OpenAI()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model

if "messages" not in st.session_state:
    st.session_state.messages = messages_base.copy()

for message in st.session_state.messages[len(messages_base):]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"][0]["text"])

if user_input := st.chat_input("What is up?"):
    user_message = {
      "role": "user",
      "content": [{
          "type": "text",
          "text": user_input
      }]
    }
    st.session_state.messages.append(user_message)
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=True,
            **params
        )
        assistant_content = st.write_stream(stream)
    assistant_message = {
      "role": "assistant",
      "content": [{
          "type": "text",
          "text": assistant_content
      }]
    }
    st.session_state.messages.append(assistant_message)
