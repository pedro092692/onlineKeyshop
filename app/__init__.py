from flask import Flask
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # flask extensions here

    # register blueprints here

    @app.route('/')
    def home():
        return 'Welcome pedro..'

    return app