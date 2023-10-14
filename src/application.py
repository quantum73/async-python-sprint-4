from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from .api import middlewares
from .api.v1 import base
from .containers import Container


def create_app() -> FastAPI:
    container = Container()
    db = container.db()
    api_prefix = container.config.get("api.prefix")

    fastapi_app = FastAPI(
        title="URL shortener app",
        docs_url="/api/openapi",
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=ORJSONResponse,
        lifespan=db.init_db,
    )
    fastapi_app.container = container
    fastapi_app.add_middleware(middlewares.BlackListMiddleware)
    fastapi_app.include_router(base.api_router, prefix=api_prefix)
    return fastapi_app


app = create_app()
