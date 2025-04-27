from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def connect(self):
        await self.db["users"].create_index("email", unique=True)
        try:
            # Test the connection
            await self.client.admin.command("ping")
            print("Connected to MongoDB")
        except ConnectionFailure:
            print("Failed to connect to MongoDB")

    async def close(self):
        await self.client.close()
        print("MongoDB connection closed")


# Singleton instance for NON dockerized app
# mongodb = MongoDB(uri="mongodb://localhost:27017", db_name="telegram-app")

# Singleton instance for DOCKERIZED application
mongodb = MongoDB(uri="mongodb://mongo:27017", db_name="telegram-app")
