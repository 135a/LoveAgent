from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "mysql+mysqlconnector://loveagent:loveagent123@localhost:3307/loveagent?charset=utf8mb4"

    # ChromaDB
    chroma_host: str = "localhost"
    chroma_port: int = 8001

    # DeepSeek
    deepseek_api_key: str = "sk-ceef8a351dd543e38db2c459b87939db"
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = "deepseek-chat"

    # JWT
    jwt_secret: str = "loveagent-jwt-secret-dev-key"
    jwt_expiration_hours: int = 24

    class Config:
        env_file = "../.env"
        extra = "allow"


settings = Settings()
