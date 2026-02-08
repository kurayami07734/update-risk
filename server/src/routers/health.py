from fastapi.routing import APIRouter


router = APIRouter(prefix="/health")


@router.get("/")
async def handle_health_check():
    return {"status": "ok"}
