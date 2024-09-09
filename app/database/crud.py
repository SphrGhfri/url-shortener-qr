from fastapi import HTTPException
from pymongo.errors import DuplicateKeyError
from typing import Dict, Any, Union, Literal


def add_user_to_database(user: Dict[str, str], user_collection) -> Dict[str, str]:
    """
    Adds a user to the database.

    Args:
        user (Dict[str, str]): The user data to add.

    Returns:
        Dict[str, str]: A success message.

    Raises:
        HTTPException: If the user already exists or there is an error adding the user.
    """
    try:
        user_collection.insert_one(user)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="User already exists.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding user: {str(e)}")

    return {"detail": "User added to the database successfully."}


def get_user_from_database(email: str, user_collection) -> Dict[str, Any]:
    """
    Retrieves a user from the database by email.

    Args:
        email (str): The email of the user to retrieve.

    Returns:
        Dict[str, Any]: The user data.

    Raises:
        HTTPException: If the user is not found or there is an error retrieving the user.
    """
    try:
        user = user_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving user: {str(e)}")

    return user


def add_url_to_database(url_data: Dict[str, str], url_collection) -> Dict[str, str]:
    """
    Adds a url to the database.

    Args:
        url (str): The url data to add.

    Returns:
        Dict[str, str]: A success message.

    Raises:
        HTTPException: If there is an error adding the url.
    """
    try:
        url_collection.insert_one(url_data)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="URL already exists.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding URL: {str(e)}")

    return {
        "short_url": url_data["short_url"],
        "qr_code": url_data["qr_url"],
        "hit_count": url_data["hit_count"],
        "short_id": url_data["short_id"],
    }


def get_url_from_database(
    input: Union[Dict[Literal["original_url"], str], Dict[Literal["short_id"], str]],
    url_collection,
) -> Dict[str, Any]:
    """
    Retrieves a url from the database by original_url or short_id.

    Args:
        input Dict[original_url, str] or Dict[short_id, str]: The field which search by in url collection and its value.

    Returns:
        Dict[str, Any]: The url data.

    Raises:
        HTTPException: If there is an error retrieving the url.
    """
    try:
        if "original_url" in input:
            url = url_collection.find_one({"original_url": input["original_url"]})
        elif "short_id" in input:
            url = url_collection.find_one({"short_id": input["short_id"]})
        else:
            raise HTTPException(status_code=404, detail="incorrect input.")

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving url: {str(e)}")

    return url


def increment_hit_count(short_id: str, url_collection) -> None:
    """
    Adds a url to the database.

    Args:
        short_id (str): The shord id of url to increment the hit count.

    Returns:
        None

    Raises:
        HTTPException: If  there is an error adding the hit count.
    """
    try:
        # Update the document
        result = url_collection.update_one(
            {"short_id": short_id}, {"$inc": {"hit_count": 1}}
        )
        # Check if the update was successful
        if not result.modified_count > 0:
            raise HTTPException(status_code=404, detail="increment hit rate failed!")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error adding url: {str(e)}")
