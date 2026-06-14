import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from the .env file
load_dotenv()

# Get the MongoDB connection URI from the environment
mongo_uri = os.getenv("MONGO_URI")

# Initialize the MongoDB client
# The client will handle connection pooling automatically
client = MongoClient(mongo_uri)

# Access the specific database
# Replace 'sp500_db' with your desired database name
db = client["sp500_db"]

# Optional: Ping the database to verify the connection
try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

# Helper to access collections
# This keeps the code clean in your routes
companies_collection = db["companies"]
sectors_collection = db["sectors"]