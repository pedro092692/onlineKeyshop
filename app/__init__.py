from flask import Flask
from flask_migrate import Migrate
from config import Config
from app.extensions import db, paypal
from app.database import DataBase
from app.extensions import CSRFProtect
from app.extensions import login_manager, turbo
from app.models.user import User
import os


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # flask extensions here

    app_db = DataBase(db, app)
    app_db.create_tables()

    # flask migrate
    migrate = Migrate(app, db)

    # login_manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_id(user_id)

    # turbo flask
    turbo.init_app(app)

    # paypal
    paypal.configure({
        "mode": "sandbox", # change live to production
        "client_id": os.environ.get('PAYPAL_CLIENT_ID'),
        "client_secret": os.environ.get('PAYPAL_CLIENT_SECRET')
    })

    #csrf
    CSRFProtect(app)

    # register blueprints here
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.posts import bp as posts_bp
    app.register_blueprint(posts_bp, url_prefix='/posts')

    from app.blueprints.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.blueprints.products import bp as product_bp
    app.register_blueprint(product_bp, url_prefix='/products')

    from app.blueprints.security import bp as security_bp
    app.register_blueprint(security_bp)

    @app.route('/test')
    def test():
        return 'Welcome pedro..'


    return app

