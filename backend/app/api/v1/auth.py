from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import create_access_token, get_current_merchant_jwt
from app.models.merchant import Merchant
from app.schemas.merchant import (
    APIKeyResponse,
    MerchantLogin,
    MerchantRegister,
    MerchantResponse,
    MerchantUpdate,
    MerchantWithKeys,
    TokenResponse,
)
from app.utils.crypto import generate_api_key, generate_webhook_secret, hash_api_key

router = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=MerchantWithKeys, status_code=201)
async def register(data: MerchantRegister, db: AsyncSession = Depends(get_db)):
    # Check if email already exists
    result = await db.execute(
        select(Merchant).where(Merchant.email == data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Generate API keys (show once, store hashed)
    api_key_live_raw = generate_api_key("pc_live")
    api_key_test_raw = generate_api_key("pc_test")

    merchant = Merchant(
        email=data.email,
        company_name=data.company_name,
        password_hash=pwd_context.hash(data.password),
        api_key_live=hash_api_key(api_key_live_raw),
        api_key_test=hash_api_key(api_key_test_raw),
        webhook_secret=generate_webhook_secret(),
    )
    db.add(merchant)
    await db.flush()
    await db.refresh(merchant)

    # Return unhashed keys only this once
    response = MerchantWithKeys.model_validate(merchant)
    response.api_key_live = api_key_live_raw
    response.api_key_test = api_key_test_raw
    return response


@router.post("/login", response_model=TokenResponse)
async def login(data: MerchantLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Merchant).where(Merchant.email == data.email)
    )
    merchant = result.scalar_one_or_none()
    if not merchant or not pwd_context.verify(data.password, merchant.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not merchant.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = create_access_token(merchant.id)
    return TokenResponse(
        access_token=token,
        merchant=MerchantResponse.model_validate(merchant),
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    merchant: Merchant = Depends(get_current_merchant_jwt),
):
    token = create_access_token(merchant.id)
    return TokenResponse(
        access_token=token,
        merchant=MerchantResponse.model_validate(merchant),
    )


merchant_router = APIRouter(prefix="/merchant", tags=["Merchant"])


@merchant_router.get("/me", response_model=MerchantResponse)
async def get_me(merchant: Merchant = Depends(get_current_merchant_jwt)):
    return MerchantResponse.model_validate(merchant)


@merchant_router.patch("/me", response_model=MerchantResponse)
async def update_me(
    data: MerchantUpdate,
    merchant: Merchant = Depends(get_current_merchant_jwt),
    db: AsyncSession = Depends(get_db),
):
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(merchant, field, value)

    await db.flush()
    await db.refresh(merchant)
    return MerchantResponse.model_validate(merchant)


@merchant_router.post("/api-keys/roll", response_model=APIKeyResponse)
async def roll_api_keys(
    merchant: Merchant = Depends(get_current_merchant_jwt),
    db: AsyncSession = Depends(get_db),
):
    api_key_live_raw = generate_api_key("pc_live")
    api_key_test_raw = generate_api_key("pc_test")

    merchant.api_key_live = hash_api_key(api_key_live_raw)
    merchant.api_key_test = hash_api_key(api_key_test_raw)

    await db.flush()

    return APIKeyResponse(
        api_key_live=api_key_live_raw,
        api_key_test=api_key_test_raw,
    )
