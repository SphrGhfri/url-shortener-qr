# Importing necessary modules and functions
from fastapi.testclient import TestClient
from app.main import app  # Importing the main FastAPI app
from app.database.connection import (
    get_user_collection,
)  # Importing the user collection dependency

import mongomock  # Importing mongomock for mocking MongoDB

# Setting up the mock MongoDB client and database
test_client = mongomock.MongoClient()
db = test_client["testDB"]  # Renamed to a more descriptive name
user_collection = db["users"]

# Creating a unique index on the 'email' field
user_collection.create_index([("email", 1)], unique=True)


def get_user_test_collection():
    """
    Returns the mock user collection for testing.
    """
    return user_collection


# Override the get_user_collection dependency to use the mock collection
app.dependency_overrides[get_user_collection] = get_user_test_collection

# Creating a TestClient instance for testing
client = TestClient(app)


class TestAuth:
    """
    Test class for authentication routes.
    """

    def test_register(self):
        """
        Test user registration endpoint.
        """
        # Sending a POST request to register a new user
        response = client.post(
            "/auth/register", json={"email": "test@example.com", "password": "pass321", "confirm_password": "pass321"}
        )
        # Asserting the response status code and detail
        assert response.status_code == 201
        assert response.json() == {"detail": "User added to the database successfully."}

        # Sending a POST request to register the same user again to test duplicate entry
        response = client.post(
            "/auth/register", json={"email": "test@example.com", "password": "pass321", "confirm_password": "pass321"}
        )
        # Asserting the response status code and detail for duplicate user
        assert response.status_code == 409
        assert response.json() == {"detail": "User already exists."}

        response = client.post(
            "/auth/register", json={"email": "test2@example.com", "password": "pass321", "confirm_password": "pass123"}
        )
        # Asserting the response status code and detail for duplicate user
        assert response.status_code == 400
        assert response.json() == {"detail": "Passwords do not match"}

    def test_login(self):
        """
        Test user login endpoint.
        """
        # Sending a POST request to login the user
        response = client.post("/auth/login", json={"email": "test@example.com", "password":"pass321"})

        # Asserting the response status code
        assert response.status_code == 200

        # Parsing the response data
        data = response.json()

        # Asserting that a token is present in the response data
        assert "token" in data

        # Sending a POST request to login with wrong password
        response = client.post("/auth/login", json={"email": "test@example.com", "password":"pass123"})
        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect Email or Password"}