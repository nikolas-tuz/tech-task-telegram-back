import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends

import routes.telegram
import routes.users
from decorators.auth_guard import auth_guard
from utils.db import mongodb

app = FastAPI()

load_dotenv()

# Enable CORS for localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("ALLOWED_HOST")],  # Allow only localhost:3000
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(routes.users.router)
app.include_router(routes.telegram.router)


@app.on_event("startup")
async def startup_db():
    await mongodb.connect()


@app.on_event("shutdown")
async def shutdown_db():
    await mongodb.close()


@app.get("/")
async def health_check():
    return {"message": "/ is healthy."}
