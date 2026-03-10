from typing import Any, Dict, Optional

import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


log = structlog.get_logger()


class StoneError(Exception):
    def __init__(self, status_code: int, detail: str, payload: dict | None = None):
        self.status_code = status_code
        self.detail = detail
        self.payload = payload or {}
        super().__init__(detail)


class StoneClient:
    def __init__(self, base_url: str, api_key: str, timeout: httpx.Timeout):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._timeout = timeout

    def _headers(self, correlation_id: str) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
            "X-Correlation-Id": correlation_id,
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type((httpx.TransportError,)),
        reraise=True,
    )
    async def create_merchant(
        self,
        payload: Dict[str, Any],
        correlation_id: str,
    ) -> Dict[str, Any]:
        """
        Cria um novo lojista (merchant) no Partner Hub.
        Retorna o StoneCode em caso de sucesso.
        """
        url = f"{self._base_url}/merchants"
        headers = self._headers(correlation_id)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.post(url, json=payload, headers=headers)

        if r.status_code >= 400:
            detail = r.text
            try:
                detail = r.json().get("detail") or r.json().get("message") or r.text
            except Exception:
                pass
            raise StoneError(r.status_code, f"Erro ao criar lojista: {detail}", self._safe_json(r))

        return self._safe_json(r)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type((httpx.TransportError,)),
        reraise=True,
    )
    async def list_merchants(
        self,
        correlation_id: str,
        page: int = 1,
        page_size: int = 50,
    ) -> Dict[str, Any]:
        """
        Lista todos os lojistas credenciados pelo parceiro.
        """
        url = f"{self._base_url}/merchants"
        headers = self._headers(correlation_id)
        params = {"page": page, "pageSize": page_size}

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.get(url, headers=headers, params=params)

        if r.status_code >= 400:
            detail = r.text
            try:
                detail = r.json().get("detail") or r.json().get("message") or r.text
            except Exception:
                pass
            raise StoneError(r.status_code, f"Erro ao listar lojistas: {detail}", self._safe_json(r))

        return self._safe_json(r)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type((httpx.TransportError,)),
        reraise=True,
    )
    async def get_merchant_details(
        self,
        stone_code: str,
        correlation_id: str,
    ) -> Dict[str, Any]:
        """
        Obtém detalhes de um lojista específico pelo StoneCode.
        """
        url = f"{self._base_url}/merchants/{stone_code}"
        headers = self._headers(correlation_id)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.get(url, headers=headers)

        if r.status_code >= 400:
            detail = r.text
            try:
                detail = r.json().get("detail") or r.json().get("message") or r.text
            except Exception:
                pass
            raise StoneError(r.status_code, f"Erro ao obter detalhes do lojista: {detail}", self._safe_json(r))

        return self._safe_json(r)

    @staticmethod
    def _safe_json(response: httpx.Response) -> Dict[str, Any]:
        try:
            return response.json()
        except Exception:
            return {"raw": response.text}
