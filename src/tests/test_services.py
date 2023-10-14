from unittest import mock

import pytest

from src.core.exceptions import ShortURLNotFoundError
from src.schemas import short_url as short_url_schemas
from .mocks import mocked_short_url_object, mocked_not_found_error, mocked_batch_short_url_objects
from ..application import app
from ..repositories.short_url import ShortURLRepository


class TestServicePingDB:
    @pytest.mark.asyncio
    async def test_ping_db_good(self):
        short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
        short_url_repository_mock.db_healthcheck.return_value = True

        with app.container.short_url_repository.override(short_url_repository_mock):
            assert await app.container.short_url_service().ping_db()

    @pytest.mark.asyncio
    async def test_ping_db_bad(self):
        short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
        short_url_repository_mock.db_healthcheck.return_value = False

        with app.container.short_url_repository.override(short_url_repository_mock):
            assert not await app.container.short_url_service().ping_db()


class TestServiceGetShortURLByID:
    @pytest.mark.asyncio
    async def test_get_short_url_by_id(self):
        short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
        short_url_repository_mock.get.return_value = mocked_short_url_object

        with app.container.short_url_repository.override(short_url_repository_mock):
            short_url = await app.container.short_url_service().get_short_url_by_id(short_id="1")
            assert short_url == mocked_short_url_object

        short_url_repository_mock.get.assert_called_once_with(idx="1")

    @pytest.mark.asyncio
    async def test_get_short_url_by_not_existed_id(self):
        short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
        short_url_repository_mock.get.side_effect = mocked_not_found_error

        with app.container.short_url_repository.override(short_url_repository_mock):
            with pytest.raises(ShortURLNotFoundError):
                await app.container.short_url_service().get_short_url_by_id(short_id="1")

        short_url_repository_mock.get.assert_called_once()


class TestServiceCreateShortURL:
    @pytest.mark.asyncio
    async def test_create_short_url(self):
        input_schema = short_url_schemas.ShortURLInput(
            short_id="1",
            original_url="https://exmaple.com/foo/",
            short_url="http://127.0.0.1:8000/",
        )
        short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
        short_url_repository_mock.create.return_value = mocked_short_url_object

        with app.container.short_url_repository.override(short_url_repository_mock):
            result = await app.container.short_url_service().create_short_url(data_to_create=input_schema)
            assert result == mocked_short_url_object

        short_url_repository_mock.create.assert_called_once_with(obj_in=input_schema)


class TestServiceBatchCreateShortURLs:
    @pytest.mark.asyncio
    async def test_batch_create_short_urls(self):
        input_schemas = [
            short_url_schemas.ShortURLInput(
                short_id="1",
                original_url="https://exmaple.com/foo/",
                short_url="http://127.0.0.1:8000/1/",
            ),
            short_url_schemas.ShortURLInput(
                short_id="2",
                original_url="https://exmaple.com/foo/",
                short_url="http://127.0.0.1:8000/2/",
            ),
        ]
        short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
        short_url_repository_mock.create_multi.return_value = mocked_batch_short_url_objects

        with app.container.short_url_repository.override(short_url_repository_mock):
            results = await app.container.short_url_service().batch_create_short_urls(data_to_create=input_schemas)
            assert results == mocked_batch_short_url_objects

        short_url_repository_mock.create_multi.assert_called_once_with(objects_in=input_schemas)


class TestServiceSetShortURLAsDelete:
    @pytest.mark.asyncio
    async def test_set_short_url_as_delete(self):
        short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
        short_url_repository_mock.delete.return_value = None

        with app.container.short_url_repository.override(short_url_repository_mock):
            await app.container.short_url_service().set_short_url_as_delete(short_url=mocked_short_url_object)

        short_url_repository_mock.delete.assert_called_once_with(short_url_obj=mocked_short_url_object)


class TestServiceClickOnShortURL:
    @pytest.mark.asyncio
    async def test_click_on_short_url(self):
        short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
        short_url_repository_mock.increase_short_url_click_count.return_value = None

        with app.container.short_url_repository.override(short_url_repository_mock):
            await app.container.short_url_service().click_on_short_url(short_url=mocked_short_url_object)

        short_url_repository_mock.increase_short_url_click_count.assert_called_once_with(
            short_url_obj=mocked_short_url_object
        )
