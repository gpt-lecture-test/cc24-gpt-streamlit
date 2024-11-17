# ################################
# Chat을 활용한 예시 (이미지 입력 가능)
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


########################################
from openai import OpenAI
import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# Title of the chatbot
st.title(title)

# Initialize OpenAI client
client = OpenAI()

# Set up OpenAI model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = messages_base.copy()

# Function to convert image to base64
def get_base64_image_url(image):
    buffered = BytesIO()
    image_format = image.format or "JPEG"
    image.save(buffered, format=image_format)
    base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/{image_format.lower()};base64,{base64_image}"

# Display chat history
for message in st.session_state.messages[len(messages_base):]:
    with st.chat_message(message["role"]):
        for content in message["content"]:
            if content["type"] == "text":
                st.markdown(content["text"])
            elif content["type"] == "image_url":
                st.image(content["image_url"]["url"], use_column_width=True)

user_input = st.chat_input("메시지를 입력하세요")  # Text input at the bottom
uploaded_image = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])  # Image uploader immediately below input

# Clear the previous image uploader when new image is uploaded
if uploaded_image:
    # Clear previous uploaded image and create a new one
    st.session_state["image_uploaded"] = uploaded_image
else:
    st.session_state["image_uploaded"] = None


if user_input :
    user_message = {"role": "user", "content": []}

    # Append text input to message
    if user_input:
        user_message["content"].append({"type": "text", "text": user_input})
        st.session_state.messages.append(user_message)
        with st.chat_message("user"):
            st.markdown(user_input)

    # Append image input to message
    if st.session_state.get("image_uploaded"):
        image = Image.open(uploaded_image)
        image_base64_url = get_base64_image_url(image)
        user_message["content"].append({"type": "image_url", "image_url": {"url": image_base64_url}})
        st.session_state.messages.append(user_message)
        with st.chat_message("user"):
            st.image(image_base64_url, use_column_width=True)

    # Process messages with GPT model
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
