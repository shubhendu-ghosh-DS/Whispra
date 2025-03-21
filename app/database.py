from pymongo import MongoClient
from .config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["messaging_app"]

users_collection = db["users"]
messages_collection = db["messages"]
