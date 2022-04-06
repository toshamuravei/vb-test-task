import logging
import sys

from pydantic import BaseSettings, validator


class Settings(BaseSettings):

    DEBUG: bool = False

    DB_MAPPED_PORT: str = "5438"
    DB_HOST: str
    POSTGRES_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URL: str = ""

    @validator('DATABASE_URL', pre=True)
    def computed_db_url(cls, _, values):
        computed_url = "postgresql://{user}:{password}@{host}:{port}/{name}"
        computed_url = computed_url.format(
            user=values["POSTGRES_USER"],
            password=values["POSTGRES_PASSWORD"],
            host=values["DB_HOST"],
            port=values["POSTGRES_PORT"],
            name=values["POSTGRES_DB"]
        )
        return computed_url


settings = Settings(_env_file='.environment')
logging.basicConfig(stream=sys.stderr, level=logging.WARN)
