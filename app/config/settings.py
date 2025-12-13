from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    database_url: str

    redis_host: str
    redis_port: int

    app_env: str
    app_debug: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
