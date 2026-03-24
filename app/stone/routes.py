from fastapi import APIRouter, Depends, Header
from typing import Optional

from app.stone.schemas import CreateMerchantRequest, MerchantResponse, ListMerchantsResponse
from app.clients.stone import StoneClient, StoneError
from app.deps import get_stone_client
import structlog

log = structlog.get_logger()
router = APIRouter(prefix="/stone", tags=["Stone Partner Hub"])


@router.post("/merchants", response_model=MerchantResponse, status_code=201)
async def create_merchant(
    payload: CreateMerchantRequest,
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-Id"),
    stone_client: StoneClient = Depends(get_stone_client),
):
    """
    Cria um novo lojista no Partner Hub da Stone.
    Retorna o StoneCode em caso de sucesso.
    """
    correlation_id = x_correlation_id or "no-correlation-id"
    
    try:
        result = await stone_client.create_merchant(
            payload=payload.model_dump(by_alias=True, exclude_none=True),
            correlation_id=correlation_id,
        )
        return result
    except StoneError as e:
        log.error("stone_create_merchant_error", status=e.status_code, detail=e.detail)
        raise


@router.get("/merchants", response_model=ListMerchantsResponse)
async def list_merchants(
    page: int = 1,
    page_size: int = 50,
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-Id"),
    stone_client: StoneClient = Depends(get_stone_client),
):
    """
    Lista todos os lojistas credenciados pelo parceiro.
    """
    correlation_id = x_correlation_id or "no-correlation-id"
    
    try:
        result = await stone_client.list_merchants(
            correlation_id=correlation_id,
            page=page,
            page_size=page_size,
        )
        return result
    except StoneError as e:
        log.error("stone_list_merchants_error", status=e.status_code, detail=e.detail)
        raise


@router.get("/merchants/{stone_code}", response_model=MerchantResponse)
async def get_merchant_details(
    stone_code: str,
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-Id"),
    stone_client: StoneClient = Depends(get_stone_client),
):
    """
    Obtém detalhes de um lojista específico pelo StoneCode.
    """
    correlation_id = x_correlation_id or "no-correlation-id"
    
    try:
        result = await stone_client.get_merchant_details(
            stone_code=stone_code,
            correlation_id=correlation_id,
        )
        return result
    except StoneError as e:
        log.error("stone_get_merchant_error", status=e.status_code, detail=e.detail, stone_code=stone_code)
        raise
