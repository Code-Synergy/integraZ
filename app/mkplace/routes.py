from fastapi import APIRouter, HTTPException, Header
from app.clients.mkplace import MkPlaceJWT
from app.mkplace.schemas import TokenRequest, TokenResponse, CustomerProfile, UpdateCustomerProfile
from app.settings import settings
import httpx
import structlog

logger = structlog.get_logger()
router = APIRouter(prefix="/mkplace", tags=["MkPlace"])


@router.post("/auth/token", response_model=TokenResponse)
async def generate_auth_token(request: TokenRequest):
    """
    Gera um JWT para autenticação SSO do cliente na MkPlace.
    Este token permite ao cliente navegar na loja, gerenciar carrinho e fazer pedidos.
    """
    try:
        token = MkPlaceJWT.generate_token(
            customer_id=request.customer_id,
            expires_in_days=request.expires_in_days
        )
        
        return TokenResponse(
            access_token=token,
            expires_in=request.expires_in_days * 86400,  # segundos
            customer_id=request.customer_id
        )
    except Exception as e:
        logger.error("mkplace_token_generation_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customer/profile", response_model=CustomerProfile)
async def get_customer_profile(authorization: str = Header(...)):
    """
    Consulta dados cadastrais do cliente na MkPlace.
    Requer token JWT no header Authorization: Bearer <token>
    """
    try:
        token = authorization.replace("Bearer ", "")
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.mkplace_api_url}/customer/profile",
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error("mkplace_get_profile_error", status=e.response.status_code, error=str(e))
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error("mkplace_get_profile_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/customer/profile")
async def update_customer_profile(
    profile: UpdateCustomerProfile,
    authorization: str = Header(...)
):
    """
    Atualiza dados cadastrais do cliente na MkPlace.
    Permite alteração de dados e adição de novos endereços.
    Requer token JWT no header Authorization: Bearer <token>
    """
    try:
        token = authorization.replace("Bearer ", "")
        
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{settings.mkplace_api_url}/customer/profile",
                json=profile.model_dump(exclude_none=True),
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error("mkplace_update_profile_error", status=e.response.status_code, error=str(e))
        raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
    except Exception as e:
        logger.error("mkplace_update_profile_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
