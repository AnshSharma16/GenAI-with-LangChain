from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

try:
    client = MongoClient(MONGO_URI)
    db = client['smart_complaints']
    collection = db['complaints']

    test_doc = {"message": "MongoDB test successful!"}
    result = collection.insert_one(test_doc)
    print("✅ Inserted document ID:", result.inserted_id)
except Exception as e:
    print("❌ MongoDB connection failed:", e)
