import os
import time
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API"))

conversation_starters = [
    "Can you start a quiz on Canadian history for me?",
    "Can we do a quiz about Canada's government?",
    "I'd like to take a quiz on Canadian culture, please.",
    "Could you give me a geography quiz on Canada?"
]

# Function to display each line of the message
def write_message_content(message):
    with st.chat_message(message.role):
        for line in message.content[0].text.value.splitlines():
            st.write(line)

# Function to handle the button click event
def on_starter_click(starter):
    # Hide the conversation starter buttons and save the selected starter
    st.session_state.hide_conversation_starter_buttons = True
    st.session_state.conversation_starter = starter

# Function to display the conversation starter buttons
def display_conversation_starter_buttons():
    # Default the conversation starter buttons to visible
    if 'hide_conversation_starter_buttons' not in st.session_state:
        st.session_state.hide_conversation_starter_buttons = False

    # Display the conversation starter buttons if they are visible
    if st.session_state.hide_conversation_starter_buttons is False:
        for starter in conversation_starters:
            st.button(starter, on_click=on_starter_click, args=[starter])


def main():
    st.title("Canada Citizenship Study Guide")

    display_conversation_starter_buttons()

    # Initialize the assistant, thread, and message lists
    if 'assistant_id' not in st.session_state:
        assistant = client.beta.assistants.retrieve(os.getenv("ASSISTANT_ID"))
        st.session_state.assistant_id = assistant.id
    if 'thread_id' not in st.session_state:
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id
    if 'thread_messages' not in st.session_state:
        # Caching the thread messages to avoid unnecessary API calls
        st.session_state.thread_messages = []

    assistant_id = st.session_state.assistant_id
    thread_id = st.session_state.thread_id
    thread_messages = st.session_state.thread_messages

    # Display all messages in the thread
    for message in thread_messages:
        write_message_content(message)

    # Set prompt from the conversation starter or user input
    conversation_starter = st.session_state.get('conversation_starter', None)
    user_input = st.chat_input("Let's get started!")
    prompt = user_input or conversation_starter

    # Handle the user's input and process it with the assistant
    if prompt:
        if conversation_starter:
            st.session_state.conversation_starter = None

        message = client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt
        )

        # Add the user's message to the cached thread messages and display it
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

        # Add the assistant's messages to the cached thread messages and display them
        messages = client.beta.threads.messages.list(thread_id, after=message.id, order="asc")
        for message in messages.data:
            thread_messages.append(message)
            write_message_content(message)


if __name__ == "__main__":
    main()