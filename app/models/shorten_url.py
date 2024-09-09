from pydantic import BaseModel, HttpUrl


# URL Model
class URL(BaseModel):
    original_url: HttpUrl
