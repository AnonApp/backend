import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres@localhost:5432/secret"
    SQLALCHEMY_TRACK_MODIFICATIONS = False