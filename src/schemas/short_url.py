import typing as tp
from datetime import datetime

from pydantic import BaseModel, AnyHttpUrl, Field

from src.core.utils import get_uuid4


class PingDatabaseOutput(BaseModel):
    db_is_works: bool


class ShortURLBase(BaseModel):
    original_url: AnyHttpUrl


class ShortURLInput(ShortURLBase):
    short_url: AnyHttpUrl
    short_id: str = Field(default_factory=get_uuid4)

    def model_post_init(self, __context: tp.Any) -> None:
        path = str(self.short_url.path).strip("/")
        self.short_url = AnyHttpUrl.build(
            scheme=self.short_url.scheme,
            host=self.short_url.host,
            port=self.short_url.port,
            path=f"{path}/{self.short_id}/",
        )


class BatchedShortURLOutput(BaseModel):
    short_id: str
    short_url: AnyHttpUrl

    class Config:
        from_attributes = True


class ShortURLInDBBase(ShortURLBase):
    short_id: str
    short_url: AnyHttpUrl

    class Config:
        from_attributes = True


class ShortURLOutput(ShortURLInDBBase):
    pass


class PaginateShortURLOutput(BaseModel):
    data: tp.Sequence[ShortURLOutput]
    offset: int
    limit: int


class ShortURLOutputFull(ShortURLInDBBase):
    last_click_at: datetime | None
    click_count: int


class ShortURLInDB(ShortURLInDBBase):
    pass
