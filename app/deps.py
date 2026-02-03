import httpx
from functools import lru_cache

from app.settings import settings
from app.clients.univers import TokenProvider, UniversClient


@lru_cache(maxsize=1)
def get_timeout() -> httpx.Timeout:
    return httpx.Timeout(
        timeout=settings.http_timeout_s,
        connect=settings.http_connect_timeout_s,
    )


@lru_cache(maxsize=1)
def get_token_provider() -> TokenProvider:
    return TokenProvider(
        token_url=settings.univers_token_url,
        client_id=settings.univers_client_id,
        client_secret=settings.univers_client_secret,
        timeout=get_timeout(),
    )


@lru_cache(maxsize=1)
def get_univers_client() -> UniversClient:
    return UniversClient(
        base_url=settings.univers_base_url,
        token_provider=get_token_provider(),
        timeout=get_timeout(),
    )
