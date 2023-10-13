import typing as tp

from .base import ServiceProtocol, ModelType, CreateSchemaType
from ..repositories.short_url import ShortURLRepository


class ShortURLService(ServiceProtocol):
    def __init__(self, short_url_repository: ShortURLRepository) -> None:
        self._repository: ShortURLRepository = short_url_repository

    async def ping_db(self) -> bool:
        return await self._repository.db_healthcheck()

    async def get_short_url_by_id(self, short_id: str) -> ModelType:
        return await self._repository.get(idx=short_id)

    async def create_short_url(self, *, data_to_create: CreateSchemaType) -> ModelType:
        return await self._repository.create(obj_in=data_to_create)

    async def batch_create_short_urls(self, data_to_create: tp.Sequence[CreateSchemaType]) -> tp.Sequence[ModelType]:
        return await self._repository.create_multi(objects_in=data_to_create)

    async def set_short_url_as_delete(self, short_url: ModelType) -> None:
        await self._repository.delete(idx=short_url.short_id)

    async def click_on_short_url(self, short_url: ModelType) -> None:
        await self._repository.increase_short_url_click_count(short_url_obj=short_url)
