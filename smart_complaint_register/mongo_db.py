import os
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB configuration  
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "complaint_system")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "complaints")

class MongoDB:
    def __init__(self):
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[DATABASE_NAME]
            self.collection = self.db[COLLECTION_NAME]
            
            # Test connection
            self.client.admin.command('ping')
            print("✅ MongoDB connection successful!")
            
        except Exception as e:
            print(f"❌ MongoDB connection failed: {str(e)}")
            print("💡 Make sure MongoDB is running or check your connection string")
            self.client = None
            self.db = None
            self.collection = None

    def is_connected(self):
        return self.client is not None

# Global MongoDB instance
mongo_instance = MongoDB()

def save_complaint(complaint_data):
    """Save complaint to MongoDB"""
    if not mongo_instance.is_connected():
        print("⚠️ MongoDB not connected - using fallback storage")
        return f"temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        complaint_data["created_at"] = datetime.now()
        complaint_data["updated_at"] = datetime.now()
        
        result = mongo_instance.collection.insert_one(complaint_data)
        complaint_id = str(result.inserted_id)
        
        print(f"✅ Complaint saved with ID: {complaint_id}")
        return complaint_id
        
    except Exception as e:
        print(f"❌ Error saving complaint: {str(e)}")
        return None

def get_all_complaints():
    """Retrieve all complaints from MongoDB"""
    if not mongo_instance.is_connected():
        print("⚠️ MongoDB not connected - returning sample data")
        return get_sample_data()
    
    try:
        complaints = list(mongo_instance.collection.find().sort("created_at", -1))
        
        for complaint in complaints:
            complaint["_id"] = str(complaint["_id"])
            
        return complaints
        
    except Exception as e:
        print(f"❌ Error fetching complaints: {str(e)}")
        return get_sample_data()

def get_complaint_by_id(complaint_id):
    """Retrieve single complaint by ID"""
    if not mongo_instance.is_connected():
        return None
    
    try:
        complaint = mongo_instance.collection.find_one({"_id": ObjectId(complaint_id)})
        
        if complaint:
            complaint["_id"] = str(complaint["_id"])
            
        return complaint
        
    except Exception as e:
        print(f"❌ Error fetching complaint: {str(e)}")
        return None

def get_complaints_by_category(category):
    """Retrieve complaints by category"""
    if not mongo_instance.is_connected():
        sample_data = get_sample_data()
        return [c for c in sample_data if c.get('category') == category]
    
    try:
        complaints = list(mongo_instance.collection.find({"category": category}).sort("created_at", -1))
        
        for complaint in complaints:
            complaint["_id"] = str(complaint["_id"])
            
        return complaints
        
    except Exception as e:
        print(f"❌ Error fetching complaints by category: {str(e)}")
        return []

def get_complaints_by_status(status):
    """Retrieve complaints by status"""
    if not mongo_instance.is_connected():
        return []
    
    try:
        complaints = list(mongo_instance.collection.find({"status": status}).sort("created_at", -1))
        
        for complaint in complaints:
            complaint["_id"] = str(complaint["_id"])
            
        return complaints
        
    except Exception as e:
        print(f"❌ Error fetching complaints by status: {str(e)}")
        return []

def update_complaint_status(complaint_id, new_status):
    """Update complaint status"""
    if not mongo_instance.is_connected():
        return False
    
    try:
        result = mongo_instance.collection.update_one(
            {"_id": ObjectId(complaint_id)},
            {"$set": {"status": new_status, "updated_at": datetime.now()}}
        )
        
        return result.modified_count > 0
        
    except Exception as e:
        print(f"❌ Error updating complaint status: {str(e)}")
        return False

def get_complaints_stats():
    """Get complaint statistics"""
    if not mongo_instance.is_connected():
        return {
            "total_complaints": 0,
            "category_breakdown": {},
            "status_breakdown": {},
            "sentiment_breakdown": {}
        }
    
    try:
        total_complaints = mongo_instance.collection.count_documents({})
        
        # Category stats
        category_pipeline = [{"$group": {"_id": "$category", "count": {"$sum": 1}}}]
        category_stats = list(mongo_instance.collection.aggregate(category_pipeline))
        
        # Status stats  
        status_pipeline = [{"$group": {"_id": "$status", "count": {"$sum": 1}}}]
        status_stats = list(mongo_instance.collection.aggregate(status_pipeline))
        
        # Sentiment stats
        sentiment_pipeline = [{"$group": {"_id": "$sentiment", "count": {"$sum": 1}}}]
        sentiment_stats = list(mongo_instance.collection.aggregate(sentiment_pipeline))
        
        return {
            "total_complaints": total_complaints,
            "category_breakdown": {item["_id"]: item["count"] for item in category_stats},
            "status_breakdown": {item["_id"]: item["count"] for item in status_stats},
            "sentiment_breakdown": {item["_id"]: item["count"] for item in sentiment_stats}
        }
        
    except Exception as e:
        print(f"❌ Error getting complaint stats: {str(e)}")
        return {}

def delete_complaint(complaint_id):
    """Delete complaint by ID"""
    if not mongo_instance.is_connected():
        return False
    
    try:
        result = mongo_instance.collection.delete_one({"_id": ObjectId(complaint_id)})
        return result.deleted_count > 0
        
    except Exception as e:
        print(f"❌ Error deleting complaint: {str(e)}")
        return False

def search_complaints(query):
    """Search complaints by text"""
    if not mongo_instance.is_connected():
        return []
    
    try:
        # Simple text search without indexing for now
        complaints = list(mongo_instance.collection.find({
            "$or": [
                {"complaint_text": {"$regex": query, "$options": "i"}},
                {"summary": {"$regex": query, "$options": "i"}},
                {"name": {"$regex": query, "$options": "i"}}
            ]
        }).sort("created_at", -1))
        
        for complaint in complaints:
            complaint["_id"] = str(complaint["_id"])
            
        return complaints
        
    except Exception as e:
        print(f"❌ Error searching complaints: {str(e)}")
        return []

def get_sample_data():
    """Return sample data when MongoDB is not available"""
    return [
        {
            "_id": "sample_1",
            "name": "John Doe",
            "email": "john@example.com", 
            "phone": "+1234567890",
            "department": "IT",
            "priority": "High",
            "complaint_text": "Login system is not working properly",
            "category": "Technical",
            "sentiment": "Negative",
            "summary": "User experiencing login issues",
            "status": "Open",
            "created_at": datetime.now()
        },
        {
            "_id": "sample_2", 
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "+1234567891", 
            "department": "Customer Service",
            "priority": "Medium",
            "complaint_text": "Response time is too slow for customer queries",
            "category": "Service",
            "sentiment": "Neutral", 
            "summary": "Customer service response time concerns",
            "status": "In Progress",
            "created_at": datetime.now()
        }
    ]

def test_connection():
    """Test MongoDB connection"""
    return mongo_instance.is_connected()

from bson import ObjectId

def update_complaint_status(complaint_id, new_status, notes):
    db = get_database()
    db[COLLECTION_NAME].update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": {
            "status": new_status,
            "resolution_notes": notes,
            "resolved_at": datetime.now() if new_status == "Resolved" else None
        }}
    )
from bson import ObjectId

def update_complaint_status(complaint_id, new_status, notes):
    db = get_database()
    db[COLLECTION_NAME].update_one(
        {"_id": ObjectId(complaint_id)},
        {"$set": {
            "status": new_status,
            "resolution_notes": notes,
            "resolved_at": datetime.now() if new_status == "Resolved" else None
        }}
    )


# Initialize on import
if __name__ == "__main__":
    print(f"MongoDB URI: {MONGO_URI}")
    print(f"Database: {DATABASE_NAME}")
    print(f"Collection: {COLLECTION_NAME}")
    print(f"Connection Status: {test_connection()}")