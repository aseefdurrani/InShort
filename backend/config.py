# backend/config.py

class Config:
    DEBUG = True
    TESTING = False
    DATABASE_URI = 'sqlite:///db.sqlite3'

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
