from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str
    echo_sql: bool = True
    test: bool = False
    project_name: str = "00.assignment"
    oauth_token_secret: str = "my_dev_secret"
    debug_logs: bool = False


settings = Settings()  # type: ignore