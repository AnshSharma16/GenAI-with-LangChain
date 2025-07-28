import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure the Gemini model with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit UI
st.header("📚 Research Tool")
st.markdown("This tool allows you to interact with Gemini AI for research purposes.")

user_input = st.text_input("Enter your research question or topic:")

if st.button("Summarize"):
    if user_input.strip() != "":
        response = model.generate_content(user_input)
        st.markdown("### 🤖 AI Response:")
        st.write(response.text)
    else:
        st.warning("Please enter a valid research topic.")
