import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

def classify_complaint(user_input):
    prompt = PromptTemplate.from_template("""
    Categorize the following customer complaint into one of these categories:
    ["Technical Issue", "Billing Problem", "Account Access", "Service Request", "Other"]

    Complaint: {complaint}
    Category:
    """)
    
    chain = prompt | llm
    result = chain.invoke({"complaint": user_input})
    return result.content.strip()
