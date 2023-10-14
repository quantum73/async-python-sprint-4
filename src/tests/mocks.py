from datetime import datetime

from fastapi import Request

from src.core.exceptions import ShortURLNotFoundError
from src.db.models import ShortURL

mocked_short_url_object = ShortURL(
    short_id="1",
    short_url="http://127.0.0.1:8000/1/",
    original_url="https://example.com/foo/",
)
mocked_full_short_url_object = ShortURL(
    short_id="1",
    short_url="http://127.0.0.1:8000/1/",
    original_url="https://example.com/foo/",
    click_count=0,
    last_click_at=datetime.now(),
)
mocked_batch_short_url_objects = [
    ShortURL(
        short_id="1",
        short_url="http://127.0.0.1:8000/1/",
        original_url="https://example.com/foo/",
    ),
    ShortURL(
        short_id="2",
        short_url="http://127.0.0.1:8000/2/",
        original_url="https://example.com/foo/",
    ),
]
mocked_not_found_error = ShortURLNotFoundError("1")


mock_request = Request(
    scope={
        "type": "http",
        "headers": {},
        "path": "/",
        "root_path": "http://127.0.0.1:8000",
    }
)
