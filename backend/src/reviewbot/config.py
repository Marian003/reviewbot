from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ReviewBot AI"
    app_version: str = "0.1.0"
    debug: bool = False
    github_token: str | None = None

    model_config = {"env_prefix": "REVIEWBOT_", "env_file": ".env", "extra": "ignore"}


settings = Settings()
