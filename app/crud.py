from fastapi import HTTPException
from passlib.hash import bcrypt
from .database import users_collection, messages_collection, friends_collection
from typing import List

def get_user_by_username(username: str):
    user = users_collection.find_one({"username": username})

    if not user:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found")


    return user

def create_user(username: str, email: str, password: str):
    hashed_password = bcrypt.hash(password)
    user_data = {
        "username": username,
        "email": email,
        "password": hashed_password,
        "active": False
    }
    users_collection.insert_one(user_data)
    return user_data

def verify_user_credentials(username: str, password: str):
    user = get_user_by_username(username)
    if not user or not bcrypt.verify(password, user["password"]):
        return None
    return user


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
    friend = get_user_by_username(username)

    if not friend:
        raise HTTPException(status_code=404, detail="Friend user not found.")

    friends_data = {
        "username": username,
        "friend": friend_username
    }

    friends_collection.insert_one(friends_data)

    return friends_data


def get_all_friends(username: str) -> List[str]:
    friends_cursor = friends_collection.find({"username": username})
    
    friends_list = [friend_doc["friend"] for friend_doc in friends_cursor]
    
    if not friends_list:
        raise HTTPException(status_code=404, detail=f"No friends found for user '{username}'.")
    
    return friends_list
