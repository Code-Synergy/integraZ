from typing import Any, Dict, Literal

import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


log = structlog.get_logger()


class AgregaError(Exception):
    def __init__(self, status_code: int, detail: str, payload: dict | None = None):
        self.status_code = status_code
        self.detail = detail
        self.payload = payload or {}
        super().__init__(detail)


class AgregaClient:
    def __init__(self, base_url: str, api_key: str, timeout: httpx.Timeout):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout

    def _headers(self, correlation_id: str) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "x-api-key": self._api_key,
            "X-Correlation-Id": correlation_id,
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type((httpx.TransportError,)),
        reraise=True,
    )
    async def create_lead(
        self,
        nome: str,
        cnpj: str,
        sede: str,
        id_plataforma: str,
        representante_legal: str,
        email: str,
        whatsapp: str,
        correlation_id: str,
    ) -> Dict[str, Any]:
        url = f"{self._base_url}/api/leads/cnpj/"
        headers = self._headers(correlation_id)
        payload = {
            "nome": nome,
            "cnpj": cnpj,
            "sede": sede,
            "id_plataforma": id_plataforma,
            "representante_legal": representante_legal,
            "email": email,
            "whatsapp": whatsapp,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.post(url, json=payload, headers=headers)

        if r.status_code >= 400:
            detail = r.text
            try:
                detail = r.json().get("detail") or r.json().get("message") or r.text
            except Exception:
                pass
            raise AgregaError(r.status_code, f"Erro ao criar lead: {detail}", self._safe_json(r))

        return self._safe_json(r)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type((httpx.TransportError,)),
        reraise=True,
    )
    async def update_lead_status(
        self,
        id_plataforma: str,
        status: Literal["ativo", "inativo"],
        correlation_id: str,
    ) -> Dict[str, Any]:
        url = f"{self._base_url}/api/leads/cnpj/atualizar_status"
        headers = self._headers(correlation_id)
        payload = {
            "id_plataforma": id_plataforma,
            "status": status,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.post(url, json=payload, headers=headers)

        if r.status_code >= 400:
            detail = r.text
            try:
                detail = r.json().get("detail") or r.json().get("message") or r.text
            except Exception:
                pass
            raise AgregaError(r.status_code, f"Erro ao atualizar status: {detail}", self._safe_json(r))

        return self._safe_json(r)

    @staticmethod
    def _safe_json(response: httpx.Response) -> Dict[str, Any]:
        try:
            return response.json()
        except Exception:
            return {"raw": response.text}
