import os
from datetime import datetime, timedelta

import bcrypt
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Response
from jose import jwt

from models.models import User
from models.users.login.request import LoginRequest
from models.users.response import UserResponse
from utils.db import mongodb

router = APIRouter(prefix="/users")

load_dotenv()

# Secret key and algorithm for JWT
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


@router.post("/register", response_model=UserResponse)
async def create_user(user: User, response: Response):
    existing_user = await mongodb.db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=403, detail="This email is taken.")

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())

    user_dict = user.dict(by_alias=True)
    user_dict["password"] = hashed_password.decode("utf-8")

    result = await mongodb.db["users"].insert_one(user_dict)

    user_dict["_id"] = result.inserted_id

    # Generate JWT token
    token_data = {
        "email": user_dict.get("email"),
        "sub": str(user_dict["_id"]),
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Set the token as a cookie
    response.set_cookie(key="access_token", value=access_token, httponly=False)

    return user_dict


@router.get("/login", response_model=UserResponse)
async def login(login_request: LoginRequest, response: Response):
    user = await mongodb.db["users"].find_one({"email": login_request.email})
    if not user:
        raise HTTPException(status_code=404, detail="Wrong email or password.")

    passwords_match = bcrypt.checkpw(login_request.password.encode("utf-8"), user.get("password").encode("utf-8"))

    if not passwords_match:
        raise HTTPException(status_code=403, detail="Wrong email or password.")

    # Generate JWT token
    token_data = {
        "sub": str(user["_id"]),
        "email": user.get("email"),
        "exp": datetime.utcnow() + timedelta(hours=1)  # Token expires in 1 hour
    }
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    # Set the token as a cookie
    response.set_cookie(key="access_token", value=access_token, httponly=False)

    user.pop("password", None)

    return user
