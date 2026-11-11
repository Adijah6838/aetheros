from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AetherOS"
    DATABASE_URL: str
    REDIS_URL: str
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"

settings = Settings()