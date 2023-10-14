from fastapi import APIRouter

from .short_url import short_url_router

api_router = APIRouter()
api_router.include_router(short_url_router, tags=["short urls"])
