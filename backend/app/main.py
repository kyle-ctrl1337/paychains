import asyncio
import json
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api.router import api_router
from app.config import get_settings
from app.database import async_session
from app.models.payment import Payment

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="PayChains API",
    description="Stripe for Crypto — API-first crypto payment infrastructure",
    version="0.1.0",
    lifespan=lifespan,
)

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
