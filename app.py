import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API"))

st.text("Hello")
st.text(os.getenv("ASSISTANT_ID"))