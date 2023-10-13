import typing as tp

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Request, Body
from pydantic import AnyHttpUrl

from src.containers import Container
from src.schemas import short_url as short_url_schemas
from src.services.short_url import ShortURLService

short_url_router = APIRouter()


@short_url_router.get(
    "/ping",
    response_model=short_url_schemas.PingDatabaseOutput,
    status_code=status.HTTP_200_OK,
)
@inject
async def ping_db(
    short_url_service: ShortURLService = Depends(Provide[Container.short_url_service]),
):
    db_is_works = await short_url_service.ping_db()
    return short_url_schemas.PingDatabaseOutput(db_is_works=db_is_works)


@short_url_router.post(
    "/",
    response_model=short_url_schemas.ShortURLOutput,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_short_url(
    request: Request,
    original_url: tp.Annotated[AnyHttpUrl, Body(embed=True)],
    short_url_service: ShortURLService = Depends(Provide[Container.short_url_service]),
):
    schema_to_create = short_url_schemas.ShortURLInput(original_url=original_url, short_url=str(request.base_url))
    new_short_url = await short_url_service.create_short_url(data_to_create=schema_to_create)
    return new_short_url
