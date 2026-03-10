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
    agrega_id_plataforma: str = Field(default="sandbox", alias="AGREGA_ID_PLATAFORMA")

    # Stone Partner Hub
    stone_base_url: str = Field(alias="STONE_BASE_URL")
    stone_api_key: str = Field(alias="STONE_API_KEY")

    # Benemed
    benemed_env: str = Field(default="hml", alias="BENEMED_ENV")
    benemed_partner_id: str = Field(default="157", alias="BENEMED_PARTNER_ID")

    # SAP Business One
    sap_base_url: str = Field(alias="SAP_BASE_URL")
    sap_company_db: str = Field(alias="SAP_COMPANY_DB")
    sap_username: str = Field(alias="SAP_USERNAME")
    sap_password: str = Field(alias="SAP_PASSWORD")
    sap_client_series: str = Field(default="71", alias="SAP_CLIENT_SERIES")
    sap_supplier_series: str = Field(default="72", alias="SAP_SUPPLIER_SERIES")
    sap_group_code: int = Field(default=106, alias="SAP_GROUP_CODE")


settings = Settings()
