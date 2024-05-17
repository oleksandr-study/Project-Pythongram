from pydantic import ConfigDict, EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str
    secret_key: str
    algorithm: str
    mail_username: EmailStr
    mail_password: str
    mail_from: EmailStr
    mail_port: int
    mail_server: str
    redis_host: str = 'localhost'
    redis_port: int = 6379
    redis_password: str | None = None
    cloudinary_name: str = 'name'
    cloudinary_api_key: str = 1234567894
    cloudinary_api_secret:str = 'secret'
    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8")


settings = Settings()