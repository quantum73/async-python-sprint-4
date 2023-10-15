from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings


class DBSecrets(BaseSettings):
    database_dsn: str = Field(env="database_dsn")

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


db_secrets = DBSecrets()
