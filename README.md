# URL Shortener with FastAPI, MongoDB, and QR Code Generation

## Overview

This is a FastAPI application provides URL shortening with authentication, generates QR codes for the shortened URLs, and tracks the number of times each shortened link is accessed. It also includes unit tests and integration tests to ensure functionality.

## Features

- User Registration: Users can register with their email and password.
- Authentication: Users can log in and receive a JWT token for accessing protected routes.
- URL Shortening: Users can shorten long URLs.
- QR Code Generation: QR codes are generated for shortened URLs.
- Hit Counter: Tracks the number of times each shortened URL is accessed.
- Testing: Includes both unit and integration tests to validate application functionality."


## 1. Install and Run With Docker Compose
You Can Configure MongoDB Connection In `app/database/connection.py` or by using environment variables from a `.env` file.
Sample `.env` file included in Repo. Remember to add this to `.gitignore` for your own usage.
```
docker compose up -d
```
## 2. Run Tests
To run tests using Docker, execute the following command:
```
docker exec Shorten_URL pytest tests -W ignore::DeprecationWarning
```

## 4. Access the API documentation in your browser:

### http://localhost:8000/docs
