from fastapi import APIRouter
from src.schema.incident_request_schema import IncidentFetchRequest
from src.services.incident_search_service import search_multiple_packages

router = APIRouter()


@router.post("/incidents")
async def fetch_incidents(payload: IncidentFetchRequest):
    incidents = await search_multiple_packages(
        package_names=payload.package_name,
        from_date=payload.from_date
    )
    return {"incidents": incidents}
