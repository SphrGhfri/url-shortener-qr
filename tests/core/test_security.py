# Importing required modules and functions
import jwt
from app.core.security import (
    JWT_SECRET,
    JWT_ALGORITHM,
    encode_jwt_token,
    decode_jwt_token,
    verify_jwt,
)


class TestSecurity:
    """
    Test class for JWT security functions.
    """

    @staticmethod
    def test_encode_jwt_token():
        """
        Test encoding a JWT token.
        """
        # Sample data to be encoded in the JWT token
        payload = {"email": "test@example.com"}

        # Encoding the payload
        token = encode_jwt_token(payload)

        # Asserting if 'token' is in the response
        assert "token" in token

    @staticmethod
    def test_decode_jwt_token():
        """
        Test decoding a JWT token.
        """
        # Sample data to be encoded in the JWT token
        payload = {"email": "test@example.com"}

        # Encoding the payload using the jwt library
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Decoding the JWT token
        decoded_data = decode_jwt_token(token)

        # Asserting the presence of expected keys and values in the decoded data
        assert "email" in decoded_data
        assert decoded_data["email"] == "test@example.com"

    @staticmethod
    def test_verify_jwt_token():
        """
        Test verifying a JWT token.
        """
        # Sample data to be encoded in the JWT token
        payload = {"email": "test@example.com"}

        # Encoding the payload using the jwt library
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

        # Verifying the JWT token
        is_verified = verify_jwt(token)

        # Asserting that the token is verified
        assert is_verified
