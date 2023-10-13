import typing as tp

from dependency_injector.wiring import inject, Provide
from fastapi import FastAPI, status
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send

from ..containers import Container


class BlackListMiddleware:
    def __init__(self, app: FastAPI) -> None:
        self._app = app

    @staticmethod
    def get_hostname_from_string(value: str | bytes) -> str:
        if isinstance(value, bytes):
            value = value.decode()

        host = value.lstrip("http://")
        host = host.lstrip("https://")
        hostname = host.split(":", maxsplit=1)[0]
        return hostname

    def get_hostname(self, headers: list[tuple[bytes, bytes]]) -> str | None:
        hostname = None
        for header_name, header_value in headers:
            if header_name.decode() == "host":
                hostname = self.get_hostname_from_string(header_value)
                break
        return hostname

    @inject
    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send,
        black_list_hosts: tp.Sequence[str] = Provide[Container.config.api.black_list_hosts],
    ) -> None:
        headers = scope.get("headers")
        if headers is None:
            await self._app(scope, receive, send)
            return

        hostname = self.get_hostname(headers=headers)
        if hostname in black_list_hosts:
            response = JSONResponse(
                content={"detail": "Host in black list!"},
                status_code=status.HTTP_403_FORBIDDEN,
            )
            await response(scope, receive, send)
        else:
            await self._app(scope, receive, send)
