import os
from flask import Flask
from services.ping import routes

def init_blueprints(app):
    try:
        #ADD Routes here
        app.register_blueprint(routes.ping_routes)
        print('✅ Blueprints Initialized')
    except Exception as e:
        print(e)
        print('❌ BLUEPRINTS ARE NOT INITIALIZED!')
        raise

def init_config(app):
    os.environ.setdefault('BACKEND_ENV', 'backend.config.DevelopmentConfig')
    try:
        app.config.from_object(os.environ['BACKEND_ENV'])
        print('✅ Config Initialized')
    except Exception as e:
        print(e)
        print('❌ CONFIG IS NOT INITIALIZED!')
        raise

def init_app():
    try:
        app = Flask(__name__)
        init_blueprints(app)
        init_config(app)
        print('App Initialized')
        return app
    except Exception as e:
        print(e)
        print('App is NOT Initialized')
        raise