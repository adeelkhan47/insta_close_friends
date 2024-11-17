from fastapi import APIRouter
# from .account import endpoints as account_endpoints

from .account import endpoints as account_endpoints
from .record import endpoints as record_endpoints
api_router = APIRouter()


api_router.include_router(
    account_endpoints.router, prefix="/account", tags=["Account"],
)

api_router.include_router(
    record_endpoints.router, prefix="/record", tags=["Record"],
)
