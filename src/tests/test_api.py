from unittest import mock

import pytest

from .mocks import mocked_short_url_object
from ..services.short_url import ShortURLService
from ..application import app
from src.schemas import short_url as short_url_schemas

API_PREFIX = "/api/v1"


class TestBlackListMiddleware:
    def test_black_list_middleware(self, client):
        with app.container.config.api.black_list_hosts.override(["127.0.0.1"]):
            response = client.get(f"{API_PREFIX}/ping")
            assert response.status_code == 403

    def test_black_list_middleware_by_allowed_host(self, client):
        response = client.get(f"{API_PREFIX}/ping")
        assert response.status_code == 200


class TestPingDatabase:
    def test_ping_db_good(self, client):
        short_url_service_mock = mock.Mock(spec=ShortURLService)
        short_url_service_mock.ping_db.return_value = True

        with app.container.short_url_service.override(short_url_service_mock):
            response = client.get(f"{API_PREFIX}/ping")
            assert response.status_code == 200
            assert response.json() == {"db_is_works": True}

    def test_ping_db_bad(self, client):
        short_url_service_mock = mock.Mock(spec=ShortURLService)
        short_url_service_mock.ping_db.return_value = False

        with app.container.short_url_service.override(short_url_service_mock):
            response = client.get(f"{API_PREFIX}/ping")
            assert response.status_code == 200
            assert response.json() == {"db_is_works": False}


# class TestGetShortURLByID:
#     def test_get_short_url_by_id(self, client):
#         short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
#         short_url_repository_mock.get_by_id.return_value = mocked_short_url_object
#
#         with app.container.short_url_repository.override(short_url_repository_mock):
#             response = client.get("/1", allow_redirects=False)
#
#         assert response.status_code == 307
#         assert response.headers["Location"] == "https://example.com/foo/"
#
#         short_url_repository_mock.get_by_id.assert_called_once_with("1")
#
#     def test_get_short_url_by_not_existed_id(self, client):
#         short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
#         short_url_repository_mock.get_by_id.side_effect = mocked_not_found_error
#
#         with app.container.short_url_repository.override(short_url_repository_mock):
#             response = client.get("/1", allow_redirects=False)
#
#         assert response.status_code == 410
#
#
class TestCreateShortURL:
    def test_create_short_url(self, client):
        short_url_service_mock = mock.Mock(spec=ShortURLService)
        short_url_service_mock.create_short_url.return_value = mocked_short_url_object

        with app.container.short_url_service.override(short_url_service_mock):
            response = client.post(f"{API_PREFIX}/", json={"original_url": "https://example.com/foo/"})

        assert response.status_code == 201
        short_url_service_mock.create_short_url.assert_called_once()

    @pytest.mark.parametrize(
        "expected_status_code,json_data",
        [
            pytest.param(422, {}, id="empty body data"),
            pytest.param(422, {"original_url": "1"}, id='wrong "original_url" field type'),
            pytest.param(422, {"foo": "https://example.com/foo/"}, id="wrong body field name"),
        ],
    )
    def test_create_short_url_by_bad_data(self, client, expected_status_code, json_data):
        response = client.post(f"{API_PREFIX}/", json=json_data)
        assert response.status_code == expected_status_code


# class TestBatchCreateShortURL:
#     def test_batch_create_short_url(self, client):
#         short_url_service_mock = mock.Mock(spec=ShortURLService)
#         short_url_service_mock.batch_create_short_url.return_value = mocked_batch_short_url_objects
#
#         with app.container.short_url_service.override(short_url_service_mock):
#             response = client.post(
#                 "/shorten",
#                 json=[
#                     {"original_url": "https://example.com/foo/"},
#                     {"original_url": "https://example.com/foo/"},
#                 ],
#             )
#
#         assert response.status_code == 201
#         assert len(response.json()) == 2
#         short_url_service_mock.batch_create_short_url.assert_called_once()
#
#     def test_batch_create_short_url_by_max_batch_size(self, client):
#         with app.container.config.api.max_batch_size.override(1):
#             response = client.post(
#                 "/shorten",
#                 json=[
#                     {"original_url": "https://example.com/foo/"},
#                     {"original_url": "https://example.com/foo/"},
#                 ],
#             )
#         assert response.status_code == 413
#
#
# class TestGetShortURLStatus:
#     def test_get_short_url_status(self, client):
#         short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
#         short_url_repository_mock.get_by_id.return_value = mocked_short_url_object
#
#         with app.container.short_url_repository.override(short_url_repository_mock):
#             response = client.get("/1/status")
#
#         assert response.status_code == 200
#
#         short_url_repository_mock.get_by_id.assert_called_once_with("1")
#
#     def test_get_short_url_status_full(self, client):
#         short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
#         short_url_repository_mock.get_by_id.return_value = mocked_full_short_url_object
#
#         with app.container.short_url_repository.override(short_url_repository_mock):
#             response = client.get("/1/status", params={"full-info": True})
#
#         assert response.status_code == 200
#
#         short_url_repository_mock.get_by_id.assert_called_once_with("1")
#
#     def test_get_short_url_by_not_existed_id(self, client):
#         short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
#         short_url_repository_mock.get_by_id.side_effect = mocked_not_found_error
#
#         with app.container.short_url_repository.override(short_url_repository_mock):
#             response = client.get("/1/status")
#
#         assert response.status_code == 410
#
#
# class TestDeleteShortURL:
#     def test_delete_short_url(self, client):
#         short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
#         short_url_repository_mock.delete.return_value = mocked_short_url_object
#
#         with app.container.short_url_repository.override(short_url_repository_mock):
#             response = client.delete("/1/delete")
#
#         assert response.status_code == 204
#         short_url_repository_mock.delete.assert_called_once()
#
#     def test_delete_already_deleted_short_url(self, client):
#         short_url_repository_mock = mock.Mock(spec=ShortURLRepository)
#         short_url_repository_mock.get_by_id.side_effect = mocked_not_found_error
#
#         with app.container.short_url_repository.override(short_url_repository_mock):
#             response = client.delete("/1/delete")
#
#         assert response.status_code == 410
#         short_url_repository_mock.get_by_id.assert_called_once()
#
#     def test_delete_not_existed_short_url(self, client):
#         response = client.delete("/73/delete")
#         assert response.status_code == 410
