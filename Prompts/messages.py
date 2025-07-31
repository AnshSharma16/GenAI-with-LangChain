from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

model=ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

messages=[
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Tell me a joke."),  # Example user input
]

result=model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages)