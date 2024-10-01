from pydantic_settings import BaseSettings
from pydantic import Extra

class Settings(BaseSettings):
    app_name: str
    app_env: str
    app_url: str

    db_conn: str
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    aws_access_key_id: str
    aws_secret_access_key: str
    aws_region_name: str
    aws_bucket: str
    aws_url: str

    jwt_secret_key: str
    jwt_refresh_key: str
    dsn_sentry: str

    class Config:
        env_file = ".env"
        extra = Extra.allow

config = Settings()