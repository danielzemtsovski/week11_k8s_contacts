from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

class Contact:
    def __init__(self,id:int, first_name:str, last_name:str, phone_number:str):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

    def contact_to_dict(self):
        return {"id":self.id,
                "first_name":self.first_name,
                "last_name":self.last_name,
                "phone_number":self.phone_number
                }

def get_database():
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command("ping")                           
        print("✓ Successfully connected to MongoDB!")
        db = client["contact_data"]
        return db
    except ConnectionFailure as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print("Make sure MongoDB is running on localhost:27017")
        return None
     
db = get_database()
collection = db["contacts"]


def create_contact(contact_data: dict):
    try:
        result = collection.insert_one(contact_data)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Error creating contact: {e}")
        return None


def get_all_contacts():
    try:
        cursor = collection.find()
        contacts = []
        for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            contacts.append(doc)
        return contacts
    except Exception as e:
        print(f"error geting contects: {e}")
        return []
    

def update_contact(id: str, contact_data: dict):
    try:
        result = collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": contact_data})
        return result.modified_count > 0
    except Exception as e:
        print(f"error updateing contects: {e}")
        return False


def delete_contact(id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"error deleteing contects: {e}")
        return False