from src.mongo.client import get_db
from src.mongo.collections import INCIDENTS
from src.models.incident_model import build_incident_document


async def save_incident(extracted_data: dict, reference_url: str):
    try:
        incident = build_incident_document(extracted_data, reference_url)

        if incident is None:
            return None

        db = get_db()
        await db[INCIDENTS].insert_one(incident)
        return incident

    except Exception as e:
        print(f"save_incident failed: {e}")
        return None
