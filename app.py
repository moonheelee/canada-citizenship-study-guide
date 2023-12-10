import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API"))
assistant_id = os.getenv("ASSISTANT_ID")

study_assistant = client.beta.assistants.retrieve(assistant_id)
print(study_assistant)

if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

thread_id = st.session_state.thread_id

thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

st.header(study_assistant.name)

for message in thread_messages.data:
    with st.chat_message(message.role):
        st.write(message.content[0].text.value)


prompt = st.chat_input("Let's get started!")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    with st.chat_message(message.role):
        st.write(message.content[0].text.value)

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    with st.spinner("Wait for it..."):
        while run.status != "completed":
            time.sleep(1)

            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

    messages = client.beta.threads.messages.list(thread_id)
    with st.chat_message(messages.data[0].role):
        st.write(messages.data[0].content[0].text.value)





