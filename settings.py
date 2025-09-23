from typing import ClassVar, List, Union

from dotenv import load_dotenv
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings

load_dotenv()

def get_api_version() -> str:
    with open("version") as version:
        return version.readline()


class APISettings(BaseSettings):    
    TITLE: str = "API AiQfome By Peregrinno"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    LOG_LEVEL: str = "info"
    VERSION: str = get_api_version()
    TIME_ZONE: str = "America/Recife"
    CORS_ORIGINS: Union[str, List[str]] = Field(..., env="API_CORS_ORIGINS")
    SECRET_KEY: str = Field(..., env="API_SECRET_KEY")
    ALGORITHM: ClassVar[str] = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 240

    @field_validator("CORS_ORIGINS", mode='before')
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    class Config:
        env_prefix = "API_"


class DatabaseSettings(BaseSettings):
    URL: str = "postgresql://postgres:De1a8@localhost:5432/aiqfome_bd"
    FALLBACK_URL: str = "sqlite:///./aiqfome.db"

    class Config:
        env_prefix = "DATABASE_"


api_settings = APISettings()
database_settings = DatabaseSettings()