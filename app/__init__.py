from flask import Flask
from flask_migrate import Migrate

from config import Config
from app.extensions import db
from app.database import DataBase
from app.extensions import CSRFProtect

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # flask extensions here
    app_db = DataBase(db, app)
    app_db.create_tables()

    # flask migrate
    migrate = Migrate(app, db)

    #csrf
    CSRFProtect(app)

    # register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/test')
    def test():
        return 'Welcome pedro..'


    return app

