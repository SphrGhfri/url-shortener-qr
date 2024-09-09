import jwt
import os
from passlib.context import CryptContext
from typing import Dict, Any
from dotenv import load_dotenv
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# Load environment variables
load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
expiration_time = os.getenv("JWT_EXPIRATION_MINUTES", "0")
JWT_EXPIRATION_MINUTES = int(expiration_time)

def verify_jwt(jwtoken: str) -> bool:
    """
    Verify the provided JWT token.

    Args:
        jwtoken (str): The JWT token to verify.

    Returns:
        bool: True if the token is valid, False otherwise.
    """
    try:
        payload = decode_jwt_token(jwtoken)
        return bool(payload)
    except Exception as e:
        print(f"Error verifying JWT token: {str(e)}")
        return False

def decode_jwt_token(token: str) -> Dict[str, str]:
    """
    Decode the provided JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        Union[Dict[str, str]]: The decoded payload if successful.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Error decoding JWT token: {str(e)}")
        raise HTTPException(status_code=401, detail="Error decoding JWT token")

def encode_jwt_token(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Encode data into a JWT token.

    Args:
        data (Dict[str, Any]): The data to encode into the token.

    Returns:
        Union[Dict[str, str], None]: The encoded token if successful, None otherwise.
    """
    try:
        encoded = jwt.encode(payload=data, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {"token": encoded}
    except Exception as e:
        print(f"Error encoding JWT token: {str(e)}")
        raise HTTPException(status_code=401, detail="Error encoding JWT token")

security = HTTPBearer()

def check_token_from_authorization(
    authorization: HTTPAuthorizationCredentials= Depends(security),
) -> bool:
    """
    Extract the token from the authorization credentials.

    Args:
        authorization (HTTPAuthorizationCredentials): The authorization credentials.

    Returns:
        str: The extracted token.

    Raises:
        HTTPException: If the token is invalid or expired.
    """
    if authorization.scheme != "Bearer":
        raise HTTPException(status_code=403, detail="Invalid authentication token")
    if not verify_jwt(authorization.credentials):
        raise HTTPException(status_code=403, detail="Invalid token or expired token")
    return True


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)