import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

st.header("Canada Citizenship Study Guide")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API"))

if 'assistant_id' not in st.session_state:
    assistant = client.beta.assistants.retrieve(os.getenv("ASSISTANT_ID"))
    print(f"Retrieve assistant: {assistant.id}")
    st.session_state.assistant_id = assistant.id

if 'thread_id' not in st.session_state:
    thread = client.beta.threads.create()
    print(f"Create a new thread: {thread.id}")
    st.session_state.thread_id = thread.id

assistant_id = st.session_state.assistant_id
thread_id = st.session_state.thread_id

thread_messages = client.beta.threads.messages.list(thread_id, order="asc")

for message in thread_messages.data:
    with st.chat_message(message.role):
        for line in message.content[0].text.value.splitlines():
            st.write(line)

prompt = st.chat_input("Let's get started!")
if prompt:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    with st.chat_message(message.role):
        for line in message.content[0].text.value.splitlines():
            st.write(line)

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
        for line in messages.data[0].content[0].text.value.splitlines():
            st.write(line)
