import typing as tp


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id: tp.Any) -> None:
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class ShortURLNotFoundError(NotFoundError):
    entity_name: str = "ShortURL"
