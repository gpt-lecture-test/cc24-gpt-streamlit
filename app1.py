# ################################
# OpenAI Assistant를 활용한 예시
# ################################

########## 구성 값 ##########

assistant_id = "asst_sNkm1WLJsosjb6PQzSkFs6l8"
title = "나만의 챗봇"
messages_base = [
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
          "text": "안녕하세요. 무엇을 도와드릴까요?"
      }]
    },
]



##############################################################################################

import streamlit as st
from openai import OpenAI
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock

# OpenAI client
client = OpenAI()

# Initialise session state to store conversation history locally to display on UI
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.title(title)

# Display messages in chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"][0]["text"])

# Textbox and streaming process
if user_input := st.chat_input("Ask me a question"):

    # Create a new thread if it does not exist
    if "thread_id" not in st.session_state:
        thread = client.beta.threads.create(messages=messages_base.copy())
        st.session_state.thread_id = thread.id

    # Display the user's query
    with st.chat_message("user"):
        st.markdown(user_input)

    # user message
    user_message = {
        "role": "user",
        "content": [{
          "type": "text",
          "text": user_input
        }]
    }

    # Store the user's query into the history
    st.session_state.chat_history.append(user_message)

    # Stream the assistant's reply
    with st.chat_message("assistant"):
        stream = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
            additional_messages=[user_message],
            stream=True
            )

        # Empty container to display the assistant's reply
        assistant_content_box = st.empty()

        # Iterate through the stream
        assistant_content = ""
        for event in stream:
            if isinstance(event, ThreadMessageDelta):
                if isinstance(event.data.delta.content[0], TextDeltaBlock):
                    assistant_content_box.empty()
                    chunk_content = event.data.delta.content[0].text.value
                    assistant_content += chunk_content
                    assistant_content_box.markdown(assistant_content)

        # assistant message
        assistant_message = {
            "role": "assistant",
            "content": [{
              "type": "text",
              "text": assistant_content
            }]
        }

        # Once the stream is over, update chat history
        st.session_state.chat_history.append(assistant_message)
