from typing import Any, Mapping
import pymongo.errors
from motor.motor_asyncio import AsyncIOMotorClient
from manticore.utils.logger import Logger


class MongoManager:
    def __init__(self, uri: str):
        self._uri = uri
        self._client = None

    async def init(self) -> bool:
        self._client = AsyncIOMotorClient(self._uri)
        Logger().info('MongoManager initialized')
        return True

    async def find(self, database: str, collection: str, query: Any) -> Any:
        return self._client[database][collection].find(query)

    async def find_one(self, database: str, collection: str, query: Any) -> Any:
        return await self._client[database][collection].find_one(query)

    async def find_last_docs(self, database: str, collection: str, query: Any, howmany: int) -> Any:
        cursor = self._client[database][collection].find(query).sort('_id', pymongo.DESCENDING)
        return await cursor.to_list(length=howmany)

    async def insert_one(self, database: str, collection: str, doc: Any) -> Any:
        try:
            result = await self._client[database][collection].insert_one(doc)
        except pymongo.errors.AutoReconnect as exc:
            Logger().error(f'MongoManager::insert_one() exception {exc}')
            return None

        return result

    async def insert_many(self, database: str, collection: str, docs: Any) -> Any:
        try:
            result = await self._client[database][collection].insert_many(docs)
        except pymongo.errors.AutoReconnect as exc:
            Logger().error(f'MongoManager::insert_many() exception {exc}')
            return None

        return result

    async def update_one(self, database: str, collection: str, query: Mapping[str, Any], values: Mapping[str, Any]) -> int:
        try:
            result = await self._client[database][collection].update_one(query, { '$set': values})
        except pymongo.errors.AutoReconnect as exc:
            Logger().error(f'MongoManager::update_one() exception {exc}')
            return 0

        return result.modified_count

    async def delete_one(self, database: str, collection: str, query: Mapping[str, Any]) -> int:
        try:
            result = await self._client[database][collection].delete_one(query)
        except pymongo.errors.AutoReconnect as exc:
            Logger().error(f'MongoManager::delete_one() exception {exc}')
            return 0

        return result.deleted_count

    async def delete_many(self, database: str, collection, query: Mapping[str, Any]) -> int:
        try:
            result = await self._client[database][collection].delete_many(query)
        except pymongo.errors.AutoReconnect as exc:
            Logger().error(f'MongoManager::delete_many() exception {exc}')
            return 0

        return result.deleted_count
