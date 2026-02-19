from fastapi.routing import APIRouter

from src.routers.health import router as health_router
from src.routers.fetch_incidents_route import router as fetch_incidents


router = APIRouter(prefix="/api")


router.include_router(health_router)
router.include_router(fetch_incidents)