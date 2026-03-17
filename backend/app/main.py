import asyncio
import json
import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy import select

from app.api.router import api_router
from app.config import get_settings
from app.database import async_session, engine, Base
import app.models  # noqa: F401 — ensure all models are registered
from app.models.payment import Payment
from app.models.merchant import Merchant

settings = get_settings()
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Add new columns if they don't exist (migrations)
    from sqlalchemy import text
    migrations = [
        "ALTER TABLE merchants ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE",
        "ALTER TABLE merchants ADD COLUMN IF NOT EXISTS xpub_key TEXT",
        "ALTER TABLE merchants ADD COLUMN IF NOT EXISTS plan VARCHAR(20) DEFAULT 'free'",
    ]
    async with engine.begin() as conn:
        for sql in migrations:
            try:
                await conn.execute(text(sql))
            except Exception:
                pass  # Column already exists or not supported

    # Ensure admin account exists
    ADMIN_EMAILS = ["kakvjgufdj@gmail.com"]
    async with async_session() as session:
        for email in ADMIN_EMAILS:
            result = await session.execute(
                select(Merchant).where(Merchant.email == email)
            )
            merchant = result.scalar_one_or_none()
            if merchant and not merchant.is_admin:
                merchant.is_admin = True
                await session.commit()

    # Log warning if admin has no xpub configured
    async with async_session() as session:
        result = await session.execute(
            select(Merchant).where(Merchant.is_admin == True)  # noqa: E712
        )
        admin = result.scalar_one_or_none()
        if admin and not admin.xpub_key:
            logger.warning("Admin merchant has no xpub_key! Plan upgrades won't work until xpub is configured.")

    yield


app = FastAPI(
    title="PayChains API",
    description="Stripe for Crypto — API-first crypto payment infrastructure",
    version="0.1.0",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.app_url, "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "paychains-api", "version": "0.1.0"}


@app.websocket("/ws/payments/{payment_id}")
async def payment_status_ws(websocket: WebSocket, payment_id: str):
    """WebSocket endpoint for real-time payment status updates."""
    await websocket.accept()

    try:
        pid = uuid.UUID(payment_id)
    except ValueError:
        await websocket.close(code=1008, reason="Invalid payment ID")
        return

    last_status = None
    last_confirmations = -1

    try:
        while True:
            async with async_session() as session:
                result = await session.execute(
                    select(Payment).where(Payment.id == pid)
                )
                payment = result.scalar_one_or_none()

                if not payment:
                    await websocket.send_json({"error": "Payment not found"})
                    break

                # Only send updates when something changes
                if payment.status != last_status or payment.confirmations != last_confirmations:
                    last_status = payment.status
                    last_confirmations = payment.confirmations
                    await websocket.send_json({
                        "payment_id": str(payment.id),
                        "status": payment.status,
                        "confirmations": payment.confirmations,
                        "required_confirmations": payment.required_confirmations,
                        "amount_usd": str(payment.amount_usd),
                        "amount_crypto": str(payment.amount_crypto) if payment.amount_crypto else None,
                        "token": payment.token,
                        "chain": payment.chain,
                        "tx_hash": payment.tx_hash,
                        "deposit_address": payment.deposit_address,
                    })

                # Stop if terminal state
                if payment.status in ("completed", "failed", "expired", "refunded"):
                    break

            await asyncio.sleep(2)

    except WebSocketDisconnect:
        pass
    except Exception:
        await websocket.close()
