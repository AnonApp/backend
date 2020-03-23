import os
import psycopg2
from flask import Flask
from app.ping import ping_bp
from app.auth import auth_bp
from app.feed import feed_bp
from config import Config

def init_blueprints(app):
    try:
        #ADD Routes here
        app.register_blueprint(ping_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(feed_bp)
        print('✅ Blueprints Initialized')
    except Exception as e:
        print(e)
        print('❌ BLUEPRINTS FAILED TO INITIALIZE!')
        raise

def init_db():
    try:
        conn = psycopg2.connect(user = "postgres", host = "localhost", port = "5432", database = "anonimus")
        cursor = conn.cursor()
        print("✅ Database Connected")

    except (Exception, psycopg2.Error) as error :
        print ("❌ Error while connecting to PostgreSQL", error)
        raise
    finally:
        if(conn):
            cursor.close()
            conn.close()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_blueprints(app)
    init_db()

    return app