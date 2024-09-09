from fastapi import HTTPException, APIRouter, Depends
from pymongo import MongoClient
from fastapi.responses import RedirectResponse, FileResponse
import shortuuid
import qrcode
import os

from app.models.shorten_url import URL
from app.database.connection import get_url_collection
from app.database.crud import (
    add_url_to_database,
    get_url_from_database,
    increment_hit_count,
)
from app.core.security import check_token_from_authorization

router = APIRouter()

BASE_URL = "http://localhost:8000/shorten"  # Centralized URL for flexibility


def generate_qr_code(link: str, short_id: str) -> str:
    """
    Generate a QR code for the given link and save it as an image.

    :param link: The link to embed in the QR code.
    :param short_id: The short identifier for the URL.
    :return: File path of the saved QR code image.
    """
    qr_img = qrcode.make(link)
    file_path = f"qr_codes/{short_id}.png"
    os.makedirs("qr_codes", exist_ok=True)  # Ensure the directory exists
    qr_img.save(file_path)
    return file_path


def create_short_id() -> str:
    """
    Generate a unique short ID for the shortened URL.

    :return: A random 6-character string.
    """
    return shortuuid.ShortUUID().random(length=6)


def format_url_data(original_url: str, short_id: str, qr_code_path: str) -> dict:
    """
    Format URL data for storage in the database.

    :param original_url: The original long URL.
    :param short_id: The unique short identifier.
    :param qr_code_path: The path to the QR code image.
    :return: A dictionary with formatted URL data.
    """
    return {
        "original_url": original_url,
        "short_url": f"{BASE_URL}/{short_id}",
        "short_id": short_id,
        "hit_count": 0,
        "qr_code": qr_code_path,
        "qr_url": f"{BASE_URL}/qr/{short_id}",
    }


@router.post("/")
def shorten_url(
    url: URL,
    url_collection: MongoClient = Depends(get_url_collection),
    authorized: bool = Depends(check_token_from_authorization),
) -> dict:
    """
    Shorten a URL, generate a QR code, and store the data in the database.

    :param url: The URL to shorten.
    :param url_collection: MongoDB collection dependency.
    :param authorized: Authorization status check.
    :return: A dictionary containing the short URL, QR code, and hit count.
    """
    existing_url = get_url_from_database(
        input={"original_url": str(url.original_url)}, url_collection=url_collection
    )

    if existing_url:
        return {
            "short_url": existing_url["short_url"],
            "qr_code": existing_url["qr_url"],
            "hit_count": existing_url["hit_count"],
            "short_id": existing_url["short_id"],
        }

    short_id = create_short_id()
    short_url = f"{BASE_URL}/{short_id}"
    qr_code_path = generate_qr_code(short_url, short_id)

    url_data = format_url_data(str(url.original_url), short_id, qr_code_path)
    return add_url_to_database(url_data=url_data, url_collection=url_collection)


@router.get("/{short_id}")
def redirect_url(
    short_id: str,
    url_collection: MongoClient = Depends(get_url_collection),
) -> RedirectResponse:
    """
    Redirect the user to the original URL associated with the short ID.

    :param short_id: The short URL identifier.
    :param url_collection: MongoDB collection dependency.
    :return: A redirect response to the original URL.
    """
    url_data = get_url_from_database(
        input={"short_id": short_id}, url_collection=url_collection
    )

    if not url_data:
        raise HTTPException(status_code=404, detail="Short URL not found")

    increment_hit_count(short_id=short_id, url_collection=url_collection)
    return RedirectResponse(url=url_data["original_url"])


@router.get("/qr/{short_id}")
def get_qr_code(
    short_id: str,
    url_collection: MongoClient = Depends(get_url_collection),
) -> FileResponse:
    """
    Return the QR code image associated with the given short ID.

    :param short_id: The short URL identifier.
    :param url_collection: MongoDB collection dependency.
    :return: A file response with the QR code image.
    """
    url_data = url_collection.find_one({"short_id": short_id})

    if not url_data or not os.path.exists(url_data["qr_code"]):
        raise HTTPException(status_code=404, detail="QR code not found")

    return FileResponse(url_data["qr_code"])
