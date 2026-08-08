from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "StudyPath AI Backend"
    app_version: str = "1.0.0"
    environment: str = "development"

    jwt_secret: str = "studypath-ai-change-this-secret"
    jwt_algorithm: str = "HS256"

    ml_service_url: str = "http://localhost:8001"
    llm_service_url: str = "http://localhost:8002"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()