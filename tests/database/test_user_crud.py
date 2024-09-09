# Importing required modules and functions
import mongomock
from app.database.crud import get_user_from_database, add_user_to_database

# Setting up the mock MongoDB client and database
test_client = mongomock.MongoClient()
db = test_client["testDB"]  # Changed to a more descriptive name
user_collection = db["users"]


class TestUserCrud:
    """
    Test class for CRUD operations on the user collection.
    """

    @staticmethod
    def test_add_user_to_database():
        """
        Test adding a user to the database.
        """
        # Sample user data to be added to the database
        new_user = {"email": "test@example.com"}

        # Adding the user to the database
        response = add_user_to_database(new_user, user_collection)

        # Asserting the response contains the expected detail
        assert "detail" in response
        assert response["detail"] == "User added to the database successfully."

    @staticmethod
    def test_get_user_from_database():
        """
        Test retrieving a user from the database.
        """
        # Sample user data to be added to the database for retrieval testing
        new_user = {"email": "test@example.com"}

        # Inserting the sample user into the mock database
        user_collection.insert_one(new_user)

        # Retrieving the user from the database
        retrieved_user = get_user_from_database("test@example.com", user_collection)

        # Asserting the retrieved user data matches the expected values
        assert "email" in retrieved_user
        assert retrieved_user["email"] == "test@example.com"
