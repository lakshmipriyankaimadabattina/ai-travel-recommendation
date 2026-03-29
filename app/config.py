from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "travel_db"
    openweather_api_key: str = ""
    secret_key: str = "dev-secret"

    class Config:
        env_file = ".env"

settings = Settings()