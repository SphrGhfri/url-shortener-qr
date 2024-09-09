from pydantic import BaseModel, EmailStr, constr
from typing import Literal

class LoginEntity(BaseModel):
    """
    Represents the login entity with an email field.
    """
    email: EmailStr
    password: constr(min_length=3)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "pass321"
            }
        }
        # Optionally, you can enable/disable the strict mode
        extra = "forbid"  # This will raise an error if unknown fields are passed


class RegisterEntity(LoginEntity):
    """
    Represents the register entity, inheriting from LoginEntity and adding a confirm_password field.
    """
    confirm_password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "pass321",
                "confirm_password": "pass321"
            }
        }
        # Optionally, you can enable/disable the strict mode
        extra = "forbid"  # This will raise an error if unknown fields are passed
