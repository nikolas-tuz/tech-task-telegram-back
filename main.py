from fastapi import FastAPI
from fastapi.params import Depends

import routes.telegram
import routes.users
from decorators.auth_guard import auth_guard
from utils.db import mongodb

app = FastAPI()

app.include_router(routes.users.router)
app.include_router(routes.telegram.router)


@app.on_event("startup")
async def startup_db():
    await mongodb.connect()


@app.on_event("shutdown")
async def shutdown_db():
    await mongodb.close()


@app.get("/")
async def health_check(user: dict = Depends(auth_guard)):
    return {"message": "/ is healthy."}
