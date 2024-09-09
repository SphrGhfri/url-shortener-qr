# MongoDB connection setup

import os
from pymongo import MongoClient
from pymongo.errors import OperationFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Environment variable keys
DATABASE_KEY = "MONGO_INITDB_DATABASE"
USERNAME_KEY = "MONGO_INITDB_ROOT_USERNAME"
PASSWORD_KEY = "MONGO_INITDB_ROOT_PASSWORD"
HOST_KEY = "MONGO_HOST"

# Load environment variables
MONGO_INITDB_DATABASE = os.getenv(DATABASE_KEY)
MONGO_INITDB_ROOT_USERNAME = os.getenv(USERNAME_KEY)
MONGO_INITDB_ROOT_PASSWORD = os.getenv(PASSWORD_KEY)
MONGO_HOST = os.getenv(HOST_KEY)


# Validate environment variables
if not all(
    [
        MONGO_INITDB_DATABASE,
        MONGO_INITDB_ROOT_USERNAME,
        MONGO_INITDB_ROOT_PASSWORD,
        MONGO_HOST,
    ]
):
    raise EnvironmentError(
        f"One or more environment variables not set: {DATABASE_KEY}, {USERNAME_KEY}, {PASSWORD_KEY}, {HOST_KEY}"
    )

try:
    # Create MongoDB client
    client = MongoClient(
        host=MONGO_HOST,
        port=27017,
        username=MONGO_INITDB_ROOT_USERNAME,
        password=MONGO_INITDB_ROOT_PASSWORD,
    )

    # Access the specified database
    db = client[MONGO_INITDB_DATABASE]

    # Define collections
    user_collection = db["users"]
    url_collection = db["urls"]

    # Create unique index on fields in collections
    user_collection.create_index([("email", 1)], unique=True)
    url_collection.create_index([("original_url", 1)], unique=True)

except OperationFailure as e:
    print(f"MongoDB operation failed: {e}")


# Dependency injection functions
def get_db():
    return db


def get_user_collection():
    return user_collection

def get_url_collection():
    return url_collection
