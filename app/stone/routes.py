from fastapi import APIRouter, Depends, Header
from typing import Optional

from app..schemas import CreateMerchantRequest, MerchantResponse, ListMerchantsResponse
from app.clients. import Client, Error
from app.deps import get__client
import structlog

log = structlog.get_logger()
router = APIRouter(prefix="/", tags=[" Partner Hub"])


@router.post("/merchants", response_model=MerchantResponse, status_code=201)
async def create_merchant(
    payload: CreateMerchantRequest,
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-Id"),
    _client: Client = Depends(get__client),
):
    """
    Cria um novo lojista no Partner Hub da .
    Retorna o Code em caso de sucesso.
    """
    correlation_id = x_correlation_id or "no-correlation-id"
    
    try:
        result = await _client.create_merchant(
            payload=payload.model_dump(by_alias=True, exclude_none=True),
            correlation_id=correlation_id,
        )
        return result
    except Error as e:
        log.error("_create_merchant_error", status=e.status_code, detail=e.detail)
        raise


@router.get("/merchants", response_model=ListMerchantsResponse)
async def list_merchants(
    page: int = 1,
    page_size: int = 50,
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-Id"),
    _client: Client = Depends(get__client),
):
    """
    Lista todos os lojistas credenciados pelo parceiro.
    """
    correlation_id = x_correlation_id or "no-correlation-id"
    
    try:
        result = await _client.list_merchants(
            correlation_id=correlation_id,
            page=page,
            page_size=page_size,
        )
        return result
    except Error as e:
        log.error("_list_merchants_error", status=e.status_code, detail=e.detail)
        raise


@router.get("/merchants/{_code}", response_model=MerchantResponse)
async def get_merchant_details(
    _code: str,
    x_correlation_id: Optional[str] = Header(None, alias="X-Correlation-Id"),
    _client: Client = Depends(get__client),
):
    """
    Obtém detalhes de um lojista específico pelo Code.
    """
    correlation_id = x_correlation_id or "no-correlation-id"
    
    try:
        result = await _client.get_merchant_details(
            _code=_code,
            correlation_id=correlation_id,
        )
        return result
    except Error as e:
        log.error("_get_merchant_error", status=e.status_code, detail=e.detail, _code=_code)
        raise
