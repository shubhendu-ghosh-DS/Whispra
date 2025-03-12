from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from passlib.hash import bcrypt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI instance
app = FastAPI()

# MongoDB connection
DB_PASSWORD = os.getenv("DB_PASSWORD")

MONGO_URI = f"mongodb+srv://mstorage044:{DB_PASSWORD}@cluster0.fnseb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client["messaging_app"]
users_collection = db["users"]
messages_collection = db["messages"]

# Pydantic models
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
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

# SIGNUP: Now includes 'active' status set to False initially
@app.post("/signup")
def signup(request: SignupRequest):
    # Check for existing username
    existing_user = users_collection.find_one({"username": request.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = bcrypt.hash(request.password)

    user_data = {
        "username": request.username,
        "email": request.email,
        "password": hashed_password,
        "active": False  # Set to False by default; admin can activate manually
    }

    users_collection.insert_one(user_data)

    return {
        "message": f"User '{request.username}' registered successfully. Activation pending."
    }

# LOGIN: Checks username, password, and if the account is active
@app.post("/login")
def login(request: LoginRequest):
    user = users_collection.find_one({"username": request.username})
    
    # If user doesn't exist or password is wrong
    if not user or not bcrypt.verify(request.password, user["password"]):
        return {"success": False, "detail": "Invalid username or password"}
    
    # Check if user is active
    if not user.get("active", False):
        return {"success": False, "detail": "User is not active. Please contact admin."}

    return {"success": True, "detail": "Login successful"}

# SEND MESSAGE: Verifies user credentials before sending
@app.post("/send_message")
def send_message(request: SendMessageRequest):
    user = users_collection.find_one({"username": request.from_username})

    if not user or not bcrypt.verify(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if sender is active
    if not user.get("active", False):
        raise HTTPException(status_code=403, detail="User is not active. Cannot send messages.")

    # Optional: Check if recipient exists
    recipient = users_collection.find_one({"username": request.to_username})
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient user not found.")

    message_data = {
        "from_username": request.from_username,
        "to_username": request.to_username,
        "message": request.message
    }

    messages_collection.insert_one(message_data)
    return {"message": "Message sent successfully"}

# SCAN MESSAGES: Verifies credentials and fetches messages
@app.post("/scan_messages")
def scan_messages(request: ScanMessagesRequest):
    user = users_collection.find_one({"username": request.username})

    if not user or not bcrypt.verify(request.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if user is active
    if not user.get("active", False):
        raise HTTPException(status_code=403, detail="User is not active. Cannot scan messages.")

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

