from fastapi import FastAPI

import routes.users
from utils.db import mongodb

app = FastAPI()

app.include_router(routes.users.router)


@app.on_event("startup")
async def startup_db():
    await mongodb.connect()


@app.on_event("shutdown")
async def shutdown_db():
    await mongodb.close()


@app.get("/")
async def healthCheck():
    return {"message": "healthy"}
