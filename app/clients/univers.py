import asyncio
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type


log = structlog.get_logger()


class UpstreamError(Exception):
    def __init__(self, status_code: int, detail: str, payload: Optional[dict] = None):
        self.status_code = status_code
        self.detail = detail
        self.payload = payload or {}
        super().__init__(detail)


@dataclass
class Token:
    access_token: str
    expires_at: float  # epoch seconds


class TokenProvider:
    """OAuth2 client_credentials com cache em memória (por processo)."""

    def __init__(self, token_url: str, client_id: str, client_secret: str, timeout: httpx.Timeout):
        self._token_url = token_url
        self._client_id = client_id
        self._client_secret = client_secret
        self._timeout = timeout

        self._lock = asyncio.Lock()
        self._token: Optional[Token] = None

    async def get(self, correlation_id: str) -> str:
        now = time.time()

        # 20s de folga para evitar expirar no meio da chamada
        if self._token and self._token.expires_at - now > 20:
            return self._token.access_token

        async with self._lock:
            now = time.time()
            if self._token and self._token.expires_at - now > 20:
                return self._token.access_token

            token = await self._fetch_token(correlation_id)
            self._token = token
            return token.access_token

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type((httpx.TransportError,)),
        reraise=True,
    )
    async def _fetch_token(self, correlation_id: str) -> Token:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            # OAuth2 Client Credentials: muitos provedores (incl. Univers) exigem Authorization: Basic
            data = {"grant_type": "client_credentials"}
            headers = {"X-Correlation-Id": correlation_id}

            r = await client.post(
                self._token_url,
                data=data,
                headers=headers,
                auth=(self._client_id, self._client_secret),
            )
            if r.status_code >= 400:
                raise UpstreamError(r.status_code, f"Falha ao obter token OAuth2: {r.text}", _safe_json(r))

            payload = r.json()
            access_token = payload.get("access_token")
            expires_in = payload.get("expires_in", 3600)

            if not access_token:
                raise UpstreamError(502, "Resposta de token inválida: access_token ausente", payload)

            return Token(access_token=access_token, expires_at=time.time() + float(expires_in))


def _safe_json(response: httpx.Response) -> Dict[str, Any]:
    try:
        return response.json()
    except Exception:
        return {"raw": response.text}


class UniversClient:
    def __init__(self, base_url: str, token_provider: TokenProvider, timeout: httpx.Timeout):
        self._base_url = base_url.rstrip("/")
        self._token_provider = token_provider
        self._timeout = timeout

    async def _headers(self, correlation_id: str) -> Dict[str, str]:
        token = await self._token_provider.get(correlation_id)
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "X-Correlation-Id": correlation_id,
        }

    def _url(self, path: str) -> str:
        return f"{self._base_url}{path}"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type((httpx.TransportError, UpstreamError)),
        reraise=True,
    )
    async def get_customize_configuration(self, store: str, correlation_id: str) -> Dict[str, Any]:
        url = self._url(f"/store/{store}/customize/configuration")
        headers = await self._headers(correlation_id)

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            r = await client.get(url, headers=headers)

        if r.status_code >= 400:
            # Para 5xx, levantamos UpstreamError para permitir retry
            payload = _safe_json(r)
            detail = payload.get("message") or payload.get("detail") or r.text
            err = UpstreamError(r.status_code, f"Upstream error {r.status_code}: {detail}", payload)
            if r.status_code >= 500:
                raise err
            # 4xx: não retry por padrão
            raise err

        return r.json()
