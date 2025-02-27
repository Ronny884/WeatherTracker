from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    weather_api_key: str

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db: str

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()