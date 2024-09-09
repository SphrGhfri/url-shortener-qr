from fastapi import APIRouter, status, Depends, HTTPException
from pymongo import MongoClient
from app.models.auth import LoginEntity, RegisterEntity
from app.database.crud import add_user_to_database, get_user_from_database
from app.database.connection import get_user_collection
from app.core.security import encode_jwt_token, hash_password, verify_password


router = APIRouter()


@router.post("/login")
async def login(
    payload: LoginEntity, user_collection: MongoClient = Depends(get_user_collection)
) -> dict:
    """
    Endpoint for user login.

    Args:
        payload (LoginEntity): The login entity containing user email.

    Returns:
        dict: JWT token if login is successful.
    """

    user = get_user_from_database(email=payload.email, user_collection=user_collection)

    # Check if the password is valid
    if not verify_password(payload.password, user['password']):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    
    user["_id"] = str(user["_id"])
    return encode_jwt_token(data=user)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterEntity, user_collection: MongoClient = Depends(get_user_collection)
) -> dict:
    """
    Endpoint for user registration.

    Args:
        payload (RegisterEntity): The registration entity containing user email and type.

    Returns:
        dict: Confirmation message if registration is successful.
    """
    # Compare password and passwordConfirm
    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match"
        )

    #  Hash the password
    payload.password = hash_password(payload.password)
    del payload.confirm_password

    return add_user_to_database(
        user={"email": payload.email, "password": payload.password},
        user_collection=user_collection,
    )
