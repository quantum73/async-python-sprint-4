from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends
from fastapi.responses import ORJSONResponse

from src.containers import Container
from src.services.short_url import ShortURLService

short_url_router = APIRouter()


@short_url_router.get("/ping", status_code=status.HTTP_200_OK)
@inject
async def ping_db(
    short_url_service: ShortURLService = Depends(Provide[Container.short_url_service]),
):
    db_is_works = await short_url_service.ping_db()
    return ORJSONResponse({"db_is_works": db_is_works})
