import typing as tp

from sqlalchemy import text


class RepositoryProtocol(tp.Protocol):
    _session_factory: tp.Any

    # def get(self, *args, **kwargs):
    #     raise NotImplementedError
    #
    # def get_multi(self, *args, **kwargs):
    #     raise NotImplementedError
    #
    # def create(self, *args, **kwargs):
    #     raise NotImplementedError
    #
    # def update(self, *args, **kwargs):
    #     raise NotImplementedError
    #
    # def delete(self, *args, **kwargs):
    #     raise NotImplementedError


class ShortURLRepository(RepositoryProtocol):
    def __init__(self, session_factory: tp.Any) -> None:
        self._session_factory = session_factory

    async def ping(self) -> bool:
        db_works = True
        async with self._session_factory() as session:
            try:
                query = await session.execute(text("SELECT 1"))
                _ = query.scalar_one_or_none()
            except Exception:
                db_works = False
        return db_works

    # def get_by_id(self, idx: str) -> ShortURL:
    #     with self._session_factory() as session:
    #         short_url = (
    #             session.query(ShortURL)
    #             .filter(
    #                 ShortURL.short_id == idx,
    #                 ShortURL.is_deleted.is_(False),
    #             )
    #             .first()
    #         )
    #         if not short_url:
    #             raise ShortURLNotFoundError(idx)
    #         return short_url

    # def create(self, short_id: str, short_url: str, original_url: str) -> ShortURL:
    #     with self._session_factory() as session:
    #         new_short_url = ShortURL(
    #             short_id=short_id,
    #             short_url=short_url,
    #             original_url=original_url,
    #         )
    #         session.add(new_short_url)
    #         session.commit()
    #         session.refresh(new_short_url)
    #         return new_short_url

    # def delete(self, short_url: ShortURL) -> None:
    #     with self._session_factory() as session:
    #         session.query(ShortURL).filter(ShortURL.short_id == short_url.short_id).update({"is_deleted": True})
    #         session.commit()

    # def increase_short_url_click_count(self, short_url: ShortURL) -> None:
    #     with self._session_factory() as session:
    #         session.query(ShortURL).filter(
    #             ShortURL.short_id == short_url.short_id,
    #         ).update(
    #             {"click_count": short_url.click_count + 1},  # type: ignore
    #         )
    #         session.commit()
