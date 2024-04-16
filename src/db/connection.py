import psycopg2
import psycopg2.extensions
import pydantic_settings
from pydantic_settings import SettingsConfigDict


class DBSettings(pydantic_settings.BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_')

    host: str
    port: int = 5432
    user: str = 'postgres'
    password: str
    name: str = 'postgres'


def get_connection(db_settings: DBSettings = None) -> psycopg2.extensions.connection:
    """Creates a psycopg2 connection to the DB with provided settings.
    If no settings provided will try to fetch them from env vars with 'DB_' prefix.
    """
    if db_settings is None:
        db_settings = DBSettings()
    return psycopg2.connect(host=db_settings.host,
                            port=db_settings.port,
                            database=db_settings.name,
                            user=db_settings.user,
                            password=db_settings.password)
