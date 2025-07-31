from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found in the environment variables.")

# Initialize the model with the API key
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key
)

# Initialize chat history
chat_history = []

# Run a chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    try:
        result = model.invoke(user_input)
        response = result.content
        print("AI:", response)

        # Save the conversation in history
        chat_history.append({"user": user_input, "ai": response})

    except Exception as e:
        print("⚠️ Error during AI invocation:", str(e))

# Show entire conversation history at the end
print("\n📜 Chat History:")
for turn in chat_history:
    print(f"You: {turn['user']}")
    print(f"AI: {turn['ai']}")
