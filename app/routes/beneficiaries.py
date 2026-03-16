from typing import Annotated, Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Request, HTTPException, Query
from pydantic import BaseModel, Field
import structlog

from app.clients.univers import UniversClient, UpstreamError
from app.deps import get_univers_client


log = structlog.get_logger()
router = APIRouter(prefix="/beneficiaries", tags=["beneficiaries"])


class Account(BaseModel):
    contractLegacyId: int
    policyLegacyId: int
    active: int
    limit: float


class Benefit(BaseModel):
    status: int
    kinshipMode: int
    ownershipMode: int
    operatorContractCodes: List[int]
    identificationNumber: str
    account: Account


class CreateBeneficiaryRequest(BaseModel):
    individualRegistration: str
    name: str
    benefits: List[Benefit]
    dependents: List[Any] = Field(default_factory=list)
    addresses: List[Any] = Field(default_factory=list)
    phones: List[Any] = Field(default_factory=list)


class UpdateBeneficiaryRequest(BaseModel):
    individualRegistration: str
    name: str
    benefits: List[Benefit]
    dependents: List[Any] = Field(default_factory=list)
    addresses: List[Any] = Field(default_factory=list)
    phones: List[Any] = Field(default_factory=list)


class UpdateStatusRequest(BaseModel):
    status: str
    policyLegacyId: int
    contractLegacyId: int
    blockOperatorCode: int


@router.post("/")
async def create_beneficiary(
    req: CreateBeneficiaryRequest,
    request: Request,
    client: Annotated[UniversClient, Depends(get_univers_client)],
):
    correlation_id = request.state.correlation_id
    try:
        return await client.create_beneficiary(
            payload=req.model_dump(),
            correlation_id=correlation_id,
        )
    except UpstreamError as e:
        log.warning("univers_error", status_code=e.status_code, detail=e.detail, correlation_id=correlation_id)
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.detail, "upstream": e.payload, "correlationId": correlation_id}
        )


@router.get("/queries")
async def get_beneficiary(
    individualRegistration: Annotated[str, Query()],
    request: Request,
    client: Annotated[UniversClient, Depends(get_univers_client)],
):
    correlation_id = request.state.correlation_id
    try:
        return await client.get_beneficiary(
            individual_registration=individualRegistration,
            correlation_id=correlation_id,
        )
    except UpstreamError as e:
        log.warning("univers_error", status_code=e.status_code, detail=e.detail, correlation_id=correlation_id)
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.detail, "upstream": e.payload, "correlationId": correlation_id}
        )


@router.put("/{beneficiary_id}")
async def update_beneficiary(
    beneficiary_id: str,
    req: UpdateBeneficiaryRequest,
    request: Request,
    client: Annotated[UniversClient, Depends(get_univers_client)],
):
    correlation_id = request.state.correlation_id
    try:
        return await client.update_beneficiary(
            beneficiary_id=beneficiary_id,
            payload=req.model_dump(),
            correlation_id=correlation_id,
        )
    except UpstreamError as e:
        log.warning("univers_error", status_code=e.status_code, detail=e.detail, correlation_id=correlation_id)
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.detail, "upstream": e.payload, "correlationId": correlation_id}
        )


@router.patch("/{beneficiary_id}/status")
async def update_beneficiary_status(
    beneficiary_id: str,
    req: UpdateStatusRequest,
    request: Request,
    client: Annotated[UniversClient, Depends(get_univers_client)],
):
    correlation_id = request.state.correlation_id
    try:
        return await client.update_beneficiary_status(
            beneficiary_id=beneficiary_id,
            payload=req.model_dump(),
            correlation_id=correlation_id,
        )
    except UpstreamError as e:
        log.warning("univers_error", status_code=e.status_code, detail=e.detail, correlation_id=correlation_id)
        raise HTTPException(
            status_code=e.status_code,
            detail={"message": e.detail, "upstream": e.payload, "correlationId": correlation_id}
        )
