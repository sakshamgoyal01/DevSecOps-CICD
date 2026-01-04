import os

class Config:
    API_TOKEN = os.getenv("API_TOKEN")
    JWT_SECRET = os.getenv("JWT_SECRET")

    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    @staticmethod
    def validate():
        missing = [k for k, v in vars(Config).items() if k.isupper() and not v]
        if missing:
            raise RuntimeError(f"Missing required environment variables: {missing}")
