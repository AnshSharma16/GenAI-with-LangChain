import os
import streamlit as st
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Streamlit UI
st.set_page_config(page_title="LangChain + Gemini Research App")
st.title("📚 AI Research Summary Tool")

# User Inputs
paper_input = st.selectbox(
    "Select a research paper topic:",
    ["Machine Learning", "Quantum Computing", "Blockchain Technology", "Artificial Intelligence", "Data Science"]
)

style_input = st.selectbox(
    "Select a writing style:",
    ["Formal", "Informal", "Technical", "Descriptive", "Persuasive"]
)

length_input = st.selectbox(
    "Select the length of the summary:",
    ["Short (1-2 paragraphs)", "Medium (3-4 paragraphs)", "Long (5+ paragraphs)"]
)

# Define LangChain prompt template
template = PromptTemplate(
    input_variables=["topic", "style", "length"],
    template="Generate a {length} summary of the research paper on {topic} in a {style} style."
)

# Format the prompt
final_prompt = template.format(
    topic=paper_input,
    style=style_input.lower(),
    length=length_input.lower()
)

# Initialize Gemini model via LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0.7
)

if st.button("Summarize"):
    with st.spinner("Generating summary..."):
        try:
            response = llm.invoke(final_prompt)
            st.subheader("📄 AI-Generated Summary")
            st.write(response.content)
        except Exception as e:
            st.error(f"❌ Error: {e}")
