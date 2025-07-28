import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

import re

def process_complaint(complaint_text):
    """
    Process complaint using Gemini AI for classification and analysis
    """
    prompt = f"""
    You are an intelligent complaint analyzer. Given a complaint, respond ONLY with JSON in this format:

    {{
        "category": "Technical, Service, Billing, Product, or General",
        "sentiment": "Positive, Neutral, or Negative",
        "summary": "2-3 sentence summary",
        "urgency_level": "1 to 10",
        "suggested_action": "clear, specific resolution step"
    }}

    Complaint: "{complaint_text}"

    IMPORTANT: Do not include explanations or preambles. Output only valid JSON.
    """

    try:
        response = model.generate_content(prompt)
        raw_output = response.text.strip()
        
        # Extract JSON using regex for safety
        match = re.search(r'\{.*\}', raw_output, re.DOTALL)
        if not match:
            raise ValueError("No valid JSON object found in response.")
        
        clean_json = match.group(0)
        result = json.loads(clean_json)
        
        # Validate required fields
        required_fields = ["category", "sentiment", "summary", "urgency_level", "suggested_action"]
        for field in required_fields:
            if field not in result:
                raise KeyError(f"Missing field: {field}")
        
        # Map urgency level to priority
        urgency = int(result["urgency_level"])
        if urgency <= 3:
            priority_text = "Low"
        elif urgency <= 6:
            priority_text = "Medium"
        elif urgency <= 8:
            priority_text = "High"
        else:
            priority_text = "Urgent"
        
        result["priority_suggestion"] = priority_text
        return result

    except Exception as e:
        print(f"[Gemini Error] {e}")
        return {
            "category": "General",
            "sentiment": "Neutral",
            "summary": "Unable to analyze complaint automatically. Manual review required.",
            "urgency_level": 5,
            "suggested_action": "Escalate to human support.",
            "priority_suggestion": "Medium"
        }

def get_complaint_insights(complaints_data):
    """
    Generate insights from multiple complaints using Gemini AI
    """
    if not complaints_data:
        return "No complaints data available for analysis."
    
    # Prepare summary data
    categories = [c.get('category', 'Unknown') for c in complaints_data]
    sentiments = [c.get('sentiment', 'Unknown') for c in complaints_data]
    
    prompt = f"""
    Analyze the following complaint data and provide insights:
    
    Categories: {categories}
    Sentiments: {sentiments}
    Total complaints: {len(complaints_data)}
    
    Provide insights in the following format:
    - Top complaint category and percentage
    - Sentiment distribution analysis
    - Key recommendations for improvement
    - Trending issues (if any patterns)
    
    Keep response concise and actionable.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Unable to generate insights: {str(e)}"

def classify_complaint_category(complaint_text):
    """
    Simple category classification function
    """
    prompt = f"""
    Classify this complaint into one category: Technical, Service, Billing, Product, or General
    
    Complaint: "{complaint_text}"
    
    Return only the category name, nothing else.
    """
    
    try:
        response = model.generate_content(prompt)
        category = response.text.strip()
        
        valid_categories = ["Technical", "Service", "Billing", "Product", "General"]
        if category in valid_categories:
            return category
        else:
            return "General"
            
    except Exception:
        return "General"

def analyze_sentiment(text):
    """
    Analyze sentiment of complaint text
    """
    prompt = f"""
    Analyze the sentiment of this text and respond with only one word: Positive, Neutral, or Negative
    
    Text: "{text}"
    """
    
    try:
        response = model.generate_content(prompt)
        sentiment = response.text.strip()
        
        valid_sentiments = ["Positive", "Neutral", "Negative"]
        if sentiment in valid_sentiments:
            return sentiment
        else:
            return "Neutral"
            
    except Exception:
        return "Neutral"

# Test function
def test_gemini_connection():
    """
    Test Gemini AI connection
    """
    try:
        test_response = model.generate_content("Say 'Connection successful'")
        return True, test_response.text
    except Exception as e:
        return False, str(e)
