from uuid import uuid4


def get_uuid4() -> str:
    return uuid4().hex
