import asyncio
from datetime import datetime
from src.mongo.client import get_db
from src.mongo.collections import INCIDENTS


async def search_single_package(package_name: str, from_date=None):
    db = get_db()
    if db is None:
        raise RuntimeError("Database not connected")

    query = {
        "package_name": {
            "$regex": package_name,
            "$options": "i"
        }
    }

    if from_date:
        query["created_at"] = {
            "$gte": from_date,
            "$lte": datetime.utcnow()
        }

    document = await db[INCIDENTS].find_one(query, {"_id": 0})

    if not document:
        return {
            "package_name": package_name,
            "incident_detected": False
        }

    return {
        "package_name": package_name,
        "incident_detected": True,
        **document
    }


async def search_multiple_packages(package_names, from_date=None):
    tasks = [
        search_single_package(name, from_date)
        for name in package_names
    ]
    return await asyncio.gather(*tasks)
