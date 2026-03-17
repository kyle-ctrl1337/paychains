from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://paychains:password@localhost:5432/paychains"
    database_url_sync: str = "postgresql://paychains:password@localhost:5432/paychains"
    redis_url: str = "redis://localhost:6379/0"

    # Auth
    jwt_secret: str = "change-me-in-production"
    jwt_expiration_minutes: int = 60

    # Wallet Security
    wallet_master_seed: str = ""
    wallet_encryption_key: str = ""

    # Blockchain RPC
    ethereum_rpc_ws: str = ""
    polygon_rpc_ws: str = ""
    bsc_rpc_ws: str = ""
    arbitrum_rpc_ws: str = ""
    base_rpc_ws: str = ""
    solana_rpc_ws: str = ""
    bitcoin_rpc_url: str = "https://blockstream.info/api"

    # Testnets
    polygon_testnet_rpc_ws: str = ""
    ethereum_testnet_rpc_ws: str = ""

    # Price Feed
    coingecko_api_key: str = ""

    # DEX
    zerox_api_key: str = ""
    oneinch_api_key: str = ""

    # Email
    resend_api_key: str = ""
    from_email: str = "payments@paychains.dev"

    # Admin
    admin_email: str = "kakvjgufdj@gmail.com"

    # App
    app_url: str = "http://localhost:5173"
    api_url: str = "http://localhost:8000"
    environment: str = "development"

    # Rate limiting
    rate_limit_free: str = "100/minute"
    rate_limit_pro: str = "1000/minute"
    rate_limit_enterprise: str = "5000/minute"

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
