from fastapi import APIRouter
# from .account import endpoints as account_endpoints

from .account import endpoints as account_endpoints
api_router = APIRouter()


api_router.include_router(
    account_endpoints.router, prefix="/account", tags=["Account"],
)
