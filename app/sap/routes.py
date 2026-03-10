from fastapi import APIRouter, HTTPException, Depends
from app.clients.sap import SAPClient
from app.sap.schemas import BusinessPartnerCreate, CardType
from app.settings import settings
import structlog

logger = structlog.get_logger()
router = APIRouter(prefix="/sap", tags=["SAP Business One"])


async def get_sap_client():
    client = SAPClient()
    try:
        yield client
    finally:
        await client.close()


@router.get("/business-partners")
async def list_business_partners(client: SAPClient = Depends(get_sap_client)):
    """Lista todos os parceiros de negócios do SAP"""
    try:
        result = await client.get_business_partners()
        return result
    except Exception as e:
        logger.error("sap_list_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/business-partners")
async def create_business_partner(
    partner: BusinessPartnerCreate,
    client: SAPClient = Depends(get_sap_client)
):
    """Cria um parceiro de negócios no SAP"""
    try:
        # Define a série baseada no tipo
        if partner.CardType == CardType.CLIENT:
            partner.Series = settings.sap_client_series
        else:
            partner.Series = settings.sap_supplier_series
        
        # Define GroupCode padrão se não informado
        if not partner.GroupCode:
            partner.GroupCode = settings.sap_group_code
        
        result = await client.create_business_partner(partner.model_dump(exclude_none=True))
        return result
    except Exception as e:
        logger.error("sap_create_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
