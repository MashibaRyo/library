from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: int = 1234
    DB_NAME: str = "postgres1"

settings = Settings()
DATABASE_URL = f"postgresql+asyncpg://postgres:1234@localhost:5432/postgres"