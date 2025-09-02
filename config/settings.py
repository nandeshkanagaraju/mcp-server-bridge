from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "company_db"

    database_type: str = "mysql"
    mcp_server_host: str = "localhost"
    mcp_server_port: int = 8080
    mcp_transport: str = "http"
    health_api_port: int = 8081
    query_timeout: int = 30
    max_query_length: int = 10000
    log_level: str = "INFO"
    log_format: str = "json"
    redis_url: str = "redis://localhost:6379/0"
    cache_ttl: int = 3600

    class Config:
        env_file = ".env"


settings = Settings()
