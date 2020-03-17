import os

class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    BASE_URL = 'http://127.0.0.1:5000'

class StagingConfig(Config):
    FLASK_ENV = 'staging'
    BASE_URL = 'http://127.0.0.1:5000'

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    BASE_URL = 'http://127.0.0.1:5000'