import os


class Config:
    DEBUG = False
    TESTING = False
    API_KEY = os.environ.get("API_KEY")


class ProductionConfig(Config):
    ENV = "production"

    # In production, we'll require the API_KEY to be set
    @property
    def API_KEY(self):
        key = os.environ.get("API_KEY")
        if not key:
            raise ValueError("API_KEY must be set in production environment")
        return key


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    API_KEY = os.environ.get("API_KEY", "key")
