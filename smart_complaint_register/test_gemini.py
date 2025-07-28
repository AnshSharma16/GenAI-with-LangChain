import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

def test_gemini_connection():
    try:
        # Get API key from .env
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env file")
            print("💡 Get your API key from: https://makersuite.google.com/app/apikey")
            return False
        
        print(f"🔑 API Key found: {api_key[:10]}...")
        
        # Configure Gemini AI
        genai.configure(api_key=api_key)
        
        print("📋 Available models:")
        models = genai.list_models()
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"  ✅ {model.name}")
        
        # Test with the recommended model
        print("\n🧪 Testing Gemini 1.5 Flash...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Say 'Hello! Gemini is working perfectly!'")
        print(f"✅ Response: {response.text}")
        
        # Test complaint processing
        print("\n🎯 Testing complaint analysis...")
        test_complaint = "The login page is not loading and I can't access my account. This is very frustrating!"
        
        prompt = f"""
        Analyze this complaint and return a JSON response:
        {{
            "category": "Technical",
            "sentiment": "Negative",
            "summary": "User experiencing login issues",
            "urgency_level": 7
        }}
        
        Complaint: "{test_complaint}"
        """
        
        response = model.generate_content(prompt)
        print(f"✅ AI Analysis: {response.text}")
        
        print("\n🎉 Gemini AI setup is working perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ Gemini AI connection failed: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your API key at: https://makersuite.google.com/app/apikey")
        print("2. Make sure your API key is added to .env file")
        print("3. Try a different model name")
        return False

if __name__ == "__main__":
    test_gemini_connection()