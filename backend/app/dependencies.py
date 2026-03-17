import uuid
from datetime import datetime, timezone

import jwt
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.models.merchant import Merchant
from app.utils.crypto import hash_api_key

settings = get_settings()


async def get_current_merchant_jwt(
    authorization: str = Header(...),
    db: AsyncSession = Depends(get_db),
) -> Merchant:
    """Extract merchant from JWT Bearer token."""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization[7:]
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        merchant_id = payload.get("sub")
        if not merchant_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(
        select(Merchant).where(Merchant.id == uuid.UUID(merchant_id))
    )
    merchant = result.scalar_one_or_none()
    if not merchant or not merchant.is_active:
        raise HTTPException(status_code=401, detail="Merchant not found or inactive")

    return merchant


async def get_current_merchant_api_key(
    x_api_key: str = Header(...),
    db: AsyncSession = Depends(get_db),
) -> Merchant:
    """Extract merchant from X-API-Key header."""
    key_hash = hash_api_key(x_api_key)

    result = await db.execute(
        select(Merchant).where(
            (Merchant.api_key_live == key_hash) | (Merchant.api_key_test == key_hash)
        )
    )
    merchant = result.scalar_one_or_none()
    if not merchant or not merchant.is_active:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return merchant


async def get_current_merchant(
    authorization: str = Header(None),
    x_api_key: str = Header(None),
    db: AsyncSession = Depends(get_db),
) -> Merchant:
    """Accept either JWT Bearer token or X-API-Key."""
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
            merchant_id = payload.get("sub")
            if not merchant_id:
                raise HTTPException(status_code=401, detail="Invalid token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        result = await db.execute(
            select(Merchant).where(Merchant.id == uuid.UUID(merchant_id))
        )
        merchant = result.scalar_one_or_none()
        if not merchant or not merchant.is_active:
            raise HTTPException(status_code=401, detail="Merchant not found or inactive")
        return merchant

    if x_api_key:
        key_hash = hash_api_key(x_api_key)
        result = await db.execute(
            select(Merchant).where(
                (Merchant.api_key_live == key_hash) | (Merchant.api_key_test == key_hash)
            )
        )
        merchant = result.scalar_one_or_none()
        if not merchant or not merchant.is_active:
            raise HTTPException(status_code=401, detail="Invalid API key")
        return merchant

    raise HTTPException(status_code=401, detail="Authentication required")


def create_access_token(merchant_id: uuid.UUID) -> str:
    """Create a JWT access token for a merchant."""
    from datetime import timedelta

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.jwt_expiration_minutes)
    payload = {
        "sub": str(merchant_id),
        "iat": now,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
