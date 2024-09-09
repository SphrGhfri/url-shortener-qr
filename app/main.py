from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes.auth import router as auth_router
from app.routes.shorten_url import router as shorten_router


app = FastAPI(title="Link Shortener API", version="1.0.0")

# CORS middleware configuration
origins = [
    os.getenv("CLIENT_ORIGIN", "http://localhost")  # Default to localhost if not set
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Auth routes
app.include_router(
    auth_router, tags=["Auth"], prefix="/auth"
)

# Shorten URL routes
app.include_router(shorten_router, tags=["Link Shortener"], prefix="/shorten")


# Health check endpoint
@app.get("/healthchecker")
def root():
    return {"message": "Healthy !", "version": "1.0.0"}

