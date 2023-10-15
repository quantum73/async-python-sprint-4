from dependency_injector import containers, providers

from .core.secrets import db_secrets
from .db.base import Database
from .repositories.short_url import ShortURLRepository
from .services.short_url import ShortURLService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[".api"])

    config = providers.Configuration(yaml_files=["config.yml", "../config.yml"])
    config.from_dict({"db": {"database_dsn": db_secrets.database_dsn}})

    db = providers.Singleton(
        Database,
        database_dsn=config.db.database_dsn,
        echo=config.db.echo,
        debug_mode=config.api.debug,
    )

    short_url_repository = providers.Factory(ShortURLRepository, session_factory=db.provided.session)
    short_url_service = providers.Factory(ShortURLService, short_url_repository=short_url_repository)
