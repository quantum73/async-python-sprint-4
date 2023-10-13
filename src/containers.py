from dependency_injector import containers, providers

from .db.base import Database
from .repositories.short_url import ShortURLRepository
from .services.short_url import ShortURLService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=[".api"])

    config = providers.Configuration(yaml_files=["config.yml", "../config.yml"])

    db = providers.Singleton(
        Database,
        database_dsn=config.db.database_dsn,
        echo=config.db.echo,
    )

    short_url_repository = providers.Factory(ShortURLRepository, session_factory=db.provided.session)
    short_url_service = providers.Factory(ShortURLService, short_url_repository=short_url_repository)
