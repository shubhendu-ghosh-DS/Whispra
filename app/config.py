import os
from dotenv import load_dotenv

load_dotenv()

DB_PASSWORD = os.getenv("DB_PASSWORD")

MONGO_URI = (
    f"mongodb+srv://mstorage044:{DB_PASSWORD}"
    "@cluster0.fnseb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
