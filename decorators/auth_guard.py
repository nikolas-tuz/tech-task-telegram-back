import os

from dotenv import load_dotenv
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from utils.db import mongodb

load_dotenv()

# Secret key and algorithm for JWT
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"

# Initialize HTTPBearer for extracting the token
security = HTTPBearer()


async def auth_guard(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Extract the JWT token from the Authorization header
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Access token is missing.")

    try:
        # Decode and verify the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        existing_user = await mongodb.db["users"].find_one({"email": payload["email"]})
        if not existing_user:
            raise HTTPException(status_code=403, detail="User does not exist.")
        existing_user.pop("password", None)

        return existing_user  # Return the decoded token payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
