import os
from flask import Flask
from app.ping import ping_bp
from app.auth import auth_bp
from config import Config

def init_blueprints(app):
    try:
        #ADD Routes here
        app.register_blueprint(ping_bp)
        app.register_blueprint(auth_bp)
        print('✅ Blueprints Initialized')
    except Exception as e:
        print(e)
        print('❌ BLUEPRINTS FAILED TO INITIALIZE!')
        raise

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_blueprints(app)

    return app