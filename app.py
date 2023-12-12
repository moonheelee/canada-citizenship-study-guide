import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Function to display each line of the message
def write_message_content(message):
    with st.chat_message(message.role):
        for line in message.content[0].text.value.splitlines():
            st.write(line)

def main():
    st.title("Canada Citizenship Study Guide")

    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API"))

    # Initialize the assistant, thread, and message lists
    if 'assistant_id' not in st.session_state:
        assistant = client.beta.assistants.retrieve(os.getenv("ASSISTANT_ID"))
        st.session_state.assistant_id = assistant.id
    if 'thread_id' not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    if 'thread_messages' not in st.session_state:
        st.session_state.thread_messages = []

    assistant_id = st.session_state.assistant_id
    thread_id = st.session_state.thread_id
    thread_messages = st.session_state.thread_messages

    # Display all messages in the thread
    for message in thread_messages:
        write_message_content(message)

    prompt = st.chat_input("Let's get started!")
    if prompt:
        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt
        )

        thread_messages.append(message)
        write_message_content(message)

        # Start the assistant's processing and wait for completion
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

        # Display the assistant's response
        messages = client.beta.threads.messages.list(thread_id, after=message.id, order="asc")
        thread_messages.append(messages.data[0])
        write_message_content(messages.data[0])


if __name__ == "__main__":
    main()