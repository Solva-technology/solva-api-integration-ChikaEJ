from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from typing import Any, Dict, List

from pymongo.results import InsertOneResult, InsertManyResult


class AsyncMongoDB:
    def __init__(self, url, db_name):
        self.client = AsyncIOMotorClient(url)
        self.db = self.client[db_name]

    async def get_collection(self, collection_name) -> AsyncIOMotorCollection:
        return await self.db[collection_name]

    async def insert_one(self, collection, data: Dict[str, Any]) -> InsertOneResult:
        return await self.db[collection].insert_one(data)

    async def insert_many(self, collection, data: List[Dict[str, Any]]) -> InsertManyResult:
        return await self.db[collection].insert_many(data)
