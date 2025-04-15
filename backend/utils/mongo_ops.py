from datetime import datetime
from config import logger, collection
import pytz
from bson import ObjectId


def save_user_data(collection, data):
    IST = pytz.timezone('Asia/Kolkata')
    data["created_at"] = datetime.now(IST)
    return collection.insert_one(data)

def save_chat_message(collection, payload):
    try:
        user_id = payload['user_id']
        message = payload['message']
        IST = pytz.timezone('Asia/Kolkata')
        
        # Convert string user_id to ObjectId
        user_object_id = ObjectId(user_id)
        
        # Update the user document by appending the new message to the chat array
        result = collection.update_one(
            {"_id": user_object_id},
            {
                "$push": {
                    "chat_history": {
                        "message": message,
                        "timestamp": datetime.now(IST)
                    }
                }
            },
            upsert=False
        )
        
        return result
    except Exception as e:
        raise Exception(f"Error saving chat message: {str(e)}")

# def update_chat(collection, user_id, msg):
#     collection.update_one(
#         {"_id": ObjectId(user_id)},
#         {"$push": {"chat_history": msg}},
#         upsert=True
#     )

# def get_chat_history(user_id, collection):
#     user_data = collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "chat": 1})
# return user_data.get("chat", []) if user_data else []
