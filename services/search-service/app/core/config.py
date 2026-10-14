from pydantic_settings import BaseSettings, SettingsConfigDict
from elasticsearch import AsyncElasticsearch

class Settings(BaseSettings):
    url: str
    index: str
    kafka_bootstrap_servers: str
    kafka_group_id: str 

    model_config = SettingsConfigDict(
        env_prefix="SEARCH_",
        extra="ignore",
    )


settings = Settings()

client = AsyncElasticsearch(settings.url)