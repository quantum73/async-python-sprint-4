import typing as tp

from fastapi.encoders import jsonable_encoder
from sqlalchemy import text, select, update as update_

from .base import RepositoryProtocol, ModelType, CreateSchemaType, UpdateSchemaType
from ..core.exceptions import ShortURLNotFoundError
from ..db.models import ShortURL


class ShortURLRepository(RepositoryProtocol):
    def __init__(self, session_factory: tp.Any) -> None:
        self._session_factory = session_factory

    async def db_healthcheck(self) -> bool:
        db_works = True
        async with self._session_factory() as session:
            try:
                query = await session.execute(text("SELECT 1"))
                query.scalar_one_or_none()
            except Exception:
                db_works = False
        return db_works

    async def get(self, *, idx: str) -> ModelType:
        async with self._session_factory() as session:
            statement = select(ShortURL).where(ShortURL.short_id == idx, ~ShortURL.is_deleted)
            query = await session.execute(statement=statement)
            short_url = query.scalar_one_or_none()
            if not short_url:
                raise ShortURLNotFoundError(idx)
            return short_url

    async def get_multi(self, *, skip=0, limit=100) -> tp.Sequence[ModelType]:
        async with self._session_factory() as session:
            statement = select(ShortURL).offset(skip).limit(limit)
            results = await session.execute(statement=statement)
            return results.scalars().all()

    async def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        async with self._session_factory() as session:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = ShortURL(**obj_in_data)
            session.add(db_obj)
            await session.commit()
            await session.refresh(db_obj)
            return db_obj

    async def create_multi(self, *, objects_in: tp.Sequence[CreateSchemaType]) -> tp.Sequence[ModelType]:
        async with self._session_factory() as session:
            db_objects = [ShortURL(**jsonable_encoder(obj)) for obj in objects_in]
            session.add_all(db_objects)
            await session.commit()
            return db_objects

    async def update(self, *, short_url_obj: ModelType, obj_in: UpdateSchemaType | tp.Mapping) -> ModelType:
        async with self._session_factory() as session:
            obj_in_data = jsonable_encoder(obj_in)
            update_statement = (
                update_(ShortURL).where(ShortURL.short_id == short_url_obj.short_id).values(**obj_in_data)
            )
            await session.execute(statement=update_statement)
            await session.commit()
            await session.refresh(short_url_obj)
            return short_url_obj

    async def delete(self, *, short_url_obj: ModelType) -> None:
        async with self._session_factory() as session:
            update_statement = (
                update_(ShortURL).where(ShortURL.short_id == short_url_obj.short_id).values(is_deleted=True)
            )
            await session.execute(statement=update_statement)
            await session.commit()

    async def increase_short_url_click_count(self, *, short_url_obj: ModelType) -> None:
        async with self._session_factory() as session:
            statement = (
                update_(ShortURL)
                .where(ShortURL.short_id == short_url_obj.short_id)
                .values(click_count=short_url_obj.click_count + 1)
            )
            await session.execute(statement=statement)
            await session.commit()
