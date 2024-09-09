# Importing required modules and functions
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database.connection import get_user_collection, get_url_collection
from app.core.security import hash_password

import mongomock

# Setting up the mock MongoDB client and database
test_client = mongomock.MongoClient()
db = test_client["testDB"]  # Renamed to a more descriptive name
user_collection = db["users"]
url_collection = db["urls"]

# Creating a unique index on the 'email' field
user_collection.create_index([("email", 1)], unique=True)


def get_user_test_collection():
    """
    Returns the mock user collection for testing.
    """
    return user_collection


def get_url_test_collection():
    """
    Returns the mock urls collection for testing.
    """
    return url_collection


# Override dependencies for testing
app.dependency_overrides[get_user_collection] = get_user_test_collection
app.dependency_overrides[get_url_collection] = get_url_test_collection

# Creating a TestClient instance for testing
client = TestClient(app)


class TestShorten:
    """
    Test class for Shorten routes.
    """

    @staticmethod
    def create_test_user(email: str, password: str):
        """
        Helper method to create a test user.
        """
        password = hash_password(password)
        user_collection.insert_one({"email": email, "password": password})

    @staticmethod
    def clear_test_db():
        """
        Helper method to clear the test database.
        """
        user_collection.delete_many({})

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Fixture to set up and tear down the test database.
        """
        # Setup: Create test users
        self.clear_test_db()
        self.create_test_user("user@example.com", "pass321")
        yield
        # Teardown: Clear the database after each test
        self.clear_test_db()

    def test_shorten_url(self):
        """
        Test the Create Short URL endpoint.
        """
        # Login to get the token
        response = client.post(
            "/auth/login", json={"email": "user@example.com", "password": "pass321"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        token = data["token"]

        # Make the request with the token but wrong input data type
        response = client.post(
            "/shorten/",
            json={"original_url": "google.com"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422

        # Make the request with the token
        response = client.post(
            "/shorten/",
            json={"original_url": "https://google.com"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()

        # Asserting the presence of expected keys in the response
        assert "short_url" in data
        assert "qr_code" in data
        assert "hit_count" in data
        assert "short_id" in data

    def test_redirect_shorten_url(self):
        """
        Test the Get Short URL and Generate QR endpoints.
        """
        # Login to get the token
        response = client.post(
            "/auth/login", json={"email": "user@example.com", "password": "pass321"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        token = data["token"]

        # Make the request to make Short URL
        response = client.post(
            "/shorten/",
            json={"original_url": "https://google.com"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()

        # Make the request to get QR code of Short URL
        response = client.get(f"/shorten/qr/{data['short_id']}")
        assert response.status_code == 200

        # Make the request to redirect from short url to original url        
        response = client.get(f"/shorten/{data['short_id']}", allow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "https://google.com/"
