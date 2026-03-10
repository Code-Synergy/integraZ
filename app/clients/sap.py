import httpx
from typing import Optional
from app.settings import settings
import structlog

logger = structlog.get_logger()


class SAPClient:
    def __init__(self):
        self.base_url = settings.sap_base_url
        self.session_id: Optional[str] = None
        self.client = httpx.AsyncClient(timeout=30.0, verify=False)

    async def login(self) -> str:
        """Autentica no SAP e retorna o session ID"""
        payload = {
            "CompanyDB": settings.sap_company_db,
            "Password": settings.sap_password,
            "UserName": settings.sap_username
        }
        
        response = await self.client.post(
            f"{self.base_url}/b1s/v1/Login",
            json=payload
        )
        response.raise_for_status()
        
        self.session_id = response.cookies.get("B1SESSION")
        logger.info("sap_login_success", session_id=self.session_id)
        return self.session_id

    async def get_business_partners(self) -> dict:
        """Lista parceiros de negócios"""
        if not self.session_id:
            await self.login()
        
        response = await self.client.get(
            f"{self.base_url}/b1s/v1/BusinessPartners",
            cookies={"B1SESSION": self.session_id}
        )
        response.raise_for_status()
        return response.json()

    async def create_business_partner(self, data: dict) -> dict:
        """Cria um parceiro de negócios"""
        if not self.session_id:
            await self.login()
        
        response = await self.client.post(
            f"{self.base_url}/b1s/v1/BusinessPartners",
            json=data,
            cookies={"B1SESSION": self.session_id}
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        """Fecha a conexão"""
        await self.client.aclose()
