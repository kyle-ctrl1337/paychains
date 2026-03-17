from fastapi import APIRouter

from app.api.v1.auth import merchant_router, router as auth_router
from app.api.v1.payment_links import router as payment_links_router
from app.api.v1.payments import router as payments_router
from app.api.v1.subscriptions import router as subscriptions_router
from app.api.v1.checkout import router as checkout_router
from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.payouts import router as payouts_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.admin import router as admin_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(merchant_router)
api_router.include_router(payment_links_router)
api_router.include_router(payments_router)
api_router.include_router(subscriptions_router)
api_router.include_router(checkout_router)
api_router.include_router(webhooks_router)
api_router.include_router(payouts_router)
api_router.include_router(analytics_router)
api_router.include_router(admin_router)
