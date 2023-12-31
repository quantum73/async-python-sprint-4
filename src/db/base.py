import typing as tp
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

Base = declarative_base()


class Database:
    def __init__(self, database_dsn: str, echo: bool = False, debug_mode: bool = False) -> None:
        self._engine = create_async_engine(database_dsn, echo=echo, future=True)
        self._async_session = sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)
        self._session_factory = scoped_session(self._async_session)
        self._debug_mode = debug_mode

    @asynccontextmanager
    async def init_db(self, app: FastAPI) -> tp.Generator[AsyncSession, None, None]:
        if self._debug_mode:
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        yield

    async def create_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_database(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    @asynccontextmanager
    async def session(self) -> tp.Generator[AsyncSession, None, None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
