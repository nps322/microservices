#from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


#ROOT_DIR = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    database_url: str
    secret_key:str
    model_config = SettingsConfigDict(
        #env_file=ROOT_DIR / ".env",
        env_prefix="AUTH_",
        extra="ignore",
    )


settings = Settings()