from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel, Field
import structlog

from app.clients.agrega import AgregaClient, AgregaError
from app.deps import get_agrega_client


log = structlog.get_logger()
router = APIRouter(prefix="/agrega", tags=["agrega"])


class CreateLeadRequest(BaseModel):
    nome: str = Field(..., description="Razão Social")
    cnpj: str = Field(..., pattern=r"^\d{14}$", description="CNPJ sem formatação (14 dígitos)")
    sede: str = Field(..., description="Endereço da sede")
    id_plataforma: str = Field(..., description="ID da plataforma (plugZ)")
    representante_legal: str
    email: str
    whatsapp: str = Field(..., pattern=r"^\d{10,11}$")


class UpdateLeadStatusRequest(BaseModel):
    id_plataforma: str
    status: Literal["ativo", "inativo"]


@router.post("/leads")
async def create_lead(
    req: CreateLeadRequest,
    request: Request,
    client: Annotated[AgregaClient, Depends(get_agrega_client)],
):
    correlation_id = request.state.correlation_id
    try:
        return await client.create_lead(
            nome=req.nome,
            cnpj=req.cnpj,
            sede=req.sede,
            id_plataforma=req.id_plataforma,
            representante_legal=req.representante_legal,
            email=req.email,
            whatsapp=req.whatsapp,
            correlation_id=correlation_id,
        )
    except AgregaError as e:
        log.warning("agrega_error", status_code=e.status_code, detail=e.detail, correlation_id=correlation_id)
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.detail, "upstream": e.payload, "correlationId": correlation_id}
        )


@router.post("/leads/status")
async def update_lead_status(
    req: UpdateLeadStatusRequest,
    request: Request,
    client: Annotated[AgregaClient, Depends(get_agrega_client)],
):
    correlation_id = request.state.correlation_id
    try:
        return await client.update_lead_status(
            id_plataforma=req.id_plataforma,
            status=req.status,
            correlation_id=correlation_id,
        )
    except AgregaError as e:
        log.warning("agrega_error", status_code=e.status_code, detail=e.detail, correlation_id=correlation_id)
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.detail, "upstream": e.payload, "correlationId": correlation_id}
        )
