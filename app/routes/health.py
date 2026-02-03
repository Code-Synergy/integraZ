from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/ready")
async def ready():
    # Aqui você pode futuramente checar dependências (DB, Redis, etc.)
    return {"status": "ready"}
