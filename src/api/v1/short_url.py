import typing as tp

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, status, Depends, Request, Body, Query
from fastapi.responses import RedirectResponse
from pydantic import AnyHttpUrl

from src.containers import Container
from src.core.exceptions import NotFoundError
from src.core.responses import GoneResponse, MaxBatchSizeResponse
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


@short_url_router.delete("/{url_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_short_url(
    url_id: str,
    short_url_service: ShortURLService = Depends(Provide[Container.short_url_service]),
):
    try:
        short_url = await short_url_service.get_short_url_by_id(short_id=url_id)
        await short_url_service.set_short_url_as_delete(short_url=short_url)
    except NotFoundError:
        return GoneResponse


@short_url_router.get("/{url_id}/status", status_code=status.HTTP_200_OK)
@inject
async def get_short_url_status(
    url_id: str,
    full_info: tp.Annotated[bool, Query(alias="full-info")] = False,
    short_url_service: ShortURLService = Depends(Provide[Container.short_url_service]),
):
    try:
        short_url = await short_url_service.get_short_url_by_id(short_id=url_id)
        if full_info:
            return short_url_schemas.ShortURLOutputFull(**short_url.__dict__)
        return short_url_schemas.ShortURLOutput(**short_url.__dict__)

    except NotFoundError:
        return GoneResponse


@short_url_router.get(
    "/{url_id}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
@inject
async def get_short_url_by_id(
    url_id: str,
    short_url_service: ShortURLService = Depends(Provide[Container.short_url_service]),
):
    try:
        short_url = await short_url_service.get_short_url_by_id(short_id=url_id)
        await short_url_service.click_on_short_url(short_url=short_url)
        return RedirectResponse(url=short_url.original_url)
    except NotFoundError:
        return GoneResponse


@short_url_router.post(
    "/shorten",
    response_model=tp.List[short_url_schemas.BatchedShortURLOutput],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def batch_create_short_url(
    request: Request,
    batch_original_urls: tp.Annotated[tp.List[short_url_schemas.ShortURLBase], Body()],
    max_batch_size: int = Depends(Provide[Container.config.api.max_batch_size.as_int()]),
    short_url_service: ShortURLService = Depends(Provide[Container.short_url_service]),
):
    if len(batch_original_urls) > max_batch_size:
        return MaxBatchSizeResponse

    base_url = str(request.base_url)
    data_to_create = [
        short_url_schemas.ShortURLInput(original_url=i.original_url, short_url=base_url)
        for i in batch_original_urls
    ]
    return await short_url_service.batch_create_short_urls(data_to_create=data_to_create)


@short_url_router.post(
    "/",
    response_model=short_url_schemas.ShortURLOutput,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_short_url(
    request: Request,
    original_url: tp.Annotated[AnyHttpUrl, Body(embed=True)],
    api_prefix: str = Depends(Provide[Container.config.api.prefix]),
    short_url_service: ShortURLService = Depends(Provide[Container.short_url_service]),
):
    api_prefix = api_prefix.strip("/")
    base_short_url = f"{request.base_url}{api_prefix}"
    schema_to_create = short_url_schemas.ShortURLInput(original_url=original_url, short_url=base_short_url)
    new_short_url = await short_url_service.create_short_url(data_to_create=schema_to_create)
    return new_short_url
