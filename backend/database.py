from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

users_collection = db["users"]
students_collection = db["students"]
marks_collection = db["marks"]
analysis_collection = db["analysis"]

print("✅ MongoDB Connected Successfully")