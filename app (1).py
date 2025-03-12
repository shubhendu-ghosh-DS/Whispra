from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.hash import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables (like db_password)
load_dotenv()

# FastAPI instance
app = FastAPI()

# MongoDB connection (environment variable for security)
DB_PASSWORD = os.getenv("DB_PASSWORD")

MONGO_URI = f"mongodb+srv://mstorage044:{DB_PASSWORD}@cluster0.fnseb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["messaging_app"]
users_collection = db["users"]
messages_collection = db["messages"]

# Pydantic models for request validation
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class SendMessageRequest(BaseModel):
    from_username: str
    password: str
    to_username: str
    message: str

class ScanMessagesRequest(BaseModel):
    username: str
    password: str

# Routes

@app.get("/")
def root():
    return {"message": "Messaging App API is running"}

@app.post("/signup")
def signup(request: SignupRequest):
    existing_user = users_collection.find_one({"username": request.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt.hash(request.password)
    user_data = {
        "username": request.username,
        "email": request.email,
        "password": hashed_password
    }

    users_collection.insert_one(user_data)
    return {"message": f"User {request.username} registered successfully"}

@app.post("/send_message")
def send_message(request: SendMessageRequest):
    user = users_collection.find_one({"username": request.from_username})
    if not user or not bcrypt.verify(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    message_data = {
        "from_username": request.from_username,
        "to_username": request.to_username,
        "message": request.message
    }

    messages_collection.insert_one(message_data)
    return {"message": "Message sent successfully"}

@app.post("/scan_messages")
def scan_messages(request: ScanMessagesRequest):
    user = users_collection.find_one({"username": request.username})
    if not user or not bcrypt.verify(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    messages_cursor = messages_collection.find({"to_username": request.username})
    messages = []
    for msg in messages_cursor:
        messages.append({
            "from_username": msg["from_username"],
            "message": msg["message"]
        })

    # Delete fetched messages
    messages_collection.delete_many({"to_username": request.username})

    return {"messages": messages} 
