import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Unified Vendor Data API"
    DEBUG: bool = True

    # Database configurations
    SQLALCHEMY_DATABASE_URI: str = "sqlite+aiosqlite:///./sqlite.db"
    POSTGRESQL_DATABASE_URI: str = "postgresql+psycopg://user:1234*@localhost/testdb"

    # Kafka configurations
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:29092"
    KAFKA_TOPIC_REQUESTS: str = "product_requests"
    KAFKA_TOPIC_RESPONSES: str = "product_responses"
    KAFKA_PRODUCT_REQ_BY_ID: str = 'product_by_id'

    # External API configurations
    VENDOR_API_URL: str = "http://localhost/makyaj-api/brand/"
    PRODUCTS_API_URL_TEMPLATE: str = "http://localhost/makyaj-api/product/brand/{brand_id}/?page={page}"
    ALL_PRODUCTS_API_URL: str = "http://localhost/makyaj-api/product/"
    BASE_API_URL: str

    # Vendor IDs
    ROCHER: str = '1'
    BEYMEN: str = '2'
    SEPHORA: str = '3'

    class Config:
        env_file = ".env"

settings = Settings()