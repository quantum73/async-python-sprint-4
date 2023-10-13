import typing as tp

from ..db.repositories import ShortURLRepository, RepositoryProtocol


class ServiceProtocol(tp.Protocol):
    _repository: RepositoryProtocol


class ShortURLService(ServiceProtocol):
    def __init__(self, short_url_repository: ShortURLRepository) -> None:
        self._repository: ShortURLRepository = short_url_repository

    # @staticmethod
    # def _generate_short_url(short_id: str, request: Request) -> str:
    #     base_url = str(request.base_url).rstrip("/")
    #     return f"{base_url}/{short_id}/"

    async def ping_db(self) -> bool:
        return await self._repository.ping()

    # def get_short_url_by_id(self, short_id: str) -> ShortURL:
    #     return self._repository.get_by_id(short_id)
    #
    # def create_short_url(self, request: Request, original_url: str) -> ShortURL:
    #     short_id = str(uuid4())
    #     short_url = self._generate_short_url(short_id=short_id, request=request)
    #     return self._repository.create(short_id=short_id, short_url=short_url, original_url=original_url)
    #
    # def batch_create_short_url(self, request: Request, original_urls: tp.List[ShortURLInput]) -> tp.List[ShortURL]:
    #     short_urls = []
    #     for url_input in original_urls:
    #         original_url = url_input.original_url.unicode_string()
    #         new_obj = self.create_short_url(request=request, original_url=original_url)
    #         short_urls.append(new_obj)
    #     return short_urls
    #
    # def set_short_url_as_delete(self, short_url: ShortURL) -> None:
    #     self._repository.delete(short_url)
    #
    # def click_on_short_url(self, short_url: ShortURL) -> None:
    #     self._repository.increase_short_url_click_count(short_url)
