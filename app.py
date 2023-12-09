import streamlit as st
from dotenv import load_dotenv
import openai
import os

# Load the .env file
load_dotenv()

# Set the OpenAI API key
openai.api_key = os.getenv('OPENAI_API')

st.text('Hello')