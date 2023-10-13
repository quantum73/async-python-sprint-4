import typing as tp

from pydantic import BaseModel

from ..repositories.base import RepositoryProtocol
from ..db.base import Base

ModelType = tp.TypeVar("ModelType", bound=Base)
CreateSchemaType = tp.TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = tp.TypeVar("UpdateSchemaType", bound=BaseModel)


class ServiceProtocol(tp.Protocol):
    _repository: RepositoryProtocol
