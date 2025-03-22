from fastapi import HTTPException
from passlib.hash import bcrypt
from .database import users_collection, messages_collection

# --- USER CRUD OPERATIONS --- #

def get_user_by_username(username: str):
    return users_collection.find_one({"username": username})

def create_user(username: str, email: str, password: str):
    hashed_password = bcrypt.hash(password)
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "active": False  # Default inactive
    }
    users_collection.insert_one(user_data)
    return user_data

def verify_user_credentials(username: str, password: str):
    user = get_user_by_username(username)
    if not user or not bcrypt.verify(password, user["password"]):
        return None
    return user

# --- MESSAGE CRUD OPERATIONS --- #

def send_message(from_username: str, to_username: str, message: str):
    recipient = get_user_by_username(to_username)
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient user not found.")
    
    message_data = {
        "from_username": from_username,
        "to_username": to_username,
        "message": message
    }
    messages_collection.insert_one(message_data)
    return message_data

def get_and_delete_messages(username: str):
    messages_cursor = messages_collection.find({"to_username": username})
    messages = [
        {"from_username": msg["from_username"], "message": msg["message"]}
        for msg in messages_cursor
    ]
    messages_collection.delete_many({"to_username": username})
    return messages


def save_friend_username(username: str, friend_username: str):
    friends_cursor = friends_collection.find({"username": username})
    friend = get_user_by_username(to_username)

    if not friend:
        raise HTTPException(status_code=404, detail="Friend user not found.")

    friends_data = {
        "username": username,
        "friend": friend_username
    }

    friends_cursor.insert_one(message_data)

    return friends_data


def get_all_friends(username: str) -> List[str]:
    # Find all documents where the user has friends
    friends_cursor = friends_collection.find({"username": username})
    
    # Convert the cursor to a list of friend usernames
    friends_list = [friend_doc["friend"] for friend_doc in friends_cursor]
    
    # Check if the user has any friends
    if not friends_list:
        raise HTTPException(status_code=404, detail=f"No friends found for user '{username}'.")
    
    return friends_list
