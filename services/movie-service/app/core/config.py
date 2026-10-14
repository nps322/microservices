from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    kafka_bootstrap_servers: str
    database_url: str
    secret_key: str
    model_config = SettingsConfigDict(
        env_prefix="MOVIE_", 
        extra="ignore",
        
    )

settings = Settings()