from fastapi import APIRouter, Depends, Request, HTTPException
import structlog

from app.clients.univers import UniversClient, UpstreamError
from app.deps import get_univers_client

log = structlog.get_logger()
router = APIRouter(prefix="/store", tags=["customize"])


@router.get("/{store}/customize/configuration")
async def get_customize_configuration(
    store: str,
    request: Request,
    client: UniversClient = Depends(get_univers_client),
):
    correlation_id = getattr(request.state, "correlation_id", "-")
    try:
        data = await client.get_customize_configuration(store=store, correlation_id=correlation_id)
        return data
    except UpstreamError as e:
        log.warning("upstream_error", status_code=e.status_code, detail=e.detail, correlation_id=correlation_id)
        raise HTTPException(status_code=e.status_code, detail={"message": e.detail, "upstream": e.payload, "correlationId": correlation_id})
