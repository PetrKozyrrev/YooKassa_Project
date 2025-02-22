from fastapi import APIRouter

from .frontend import router as frontend
from .payment import router as payment_router

backend_router = APIRouter(prefix="/api")
frontend_router = APIRouter()

frontend_router.include_router(frontend)
backend_router.include_router(payment_router)