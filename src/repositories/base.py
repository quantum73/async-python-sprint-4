import typing as tp

from pydantic import BaseModel

from ..db.base import Base

ModelType = tp.TypeVar("ModelType", bound=Base)
CreateSchemaType = tp.TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = tp.TypeVar("UpdateSchemaType", bound=BaseModel)


class RepositoryProtocol(tp.Protocol):
    def get(self, *args, **kwargs):
        raise NotImplementedError

    def get_multi(self, *args, **kwargs):
        raise NotImplementedError

    def create(self, *args, **kwargs):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        raise NotImplementedError

    def delete(self, *args, **kwargs):
        raise NotImplementedError
