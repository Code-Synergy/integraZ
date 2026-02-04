from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = Field(default="univers-proxy", alias="APP_NAME")
    app_env: str = Field(default="dev", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # HTTP
    http_timeout_s: float = Field(default=20.0, alias="HTTP_TIMEOUT_S")
    http_connect_timeout_s: float = Field(default=5.0, alias="HTTP_CONNECT_TIMEOUT_S")

    # Upstream (Univers)
    univers_base_url: str = Field(alias="UNIVERS_BASE_URL")
    univers_token_url: str = Field(alias="UNIVERS_TOKEN_URL")
    univers_client_id: str = Field(alias="UNIVERS_CLIENT_ID")
    univers_client_secret: str = Field(alias="UNIVERS_CLIENT_SECRET")

    univers_default_store: str = Field(default="DROGASIL", alias="UNIVERS_DEFAULT_STORE")

    # Agrega
    agrega_base_url: str = Field(alias="AGREGA_BASE_URL")
    agrega_api_key: str = Field(alias="AGREGA_API_KEY")


settings = Settings()
