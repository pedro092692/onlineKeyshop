import os
from app.models.post import Post
from app.models.user import User
from app.models.platforms import Platform
from app.models.key import Key
from app.models.category import Category
from app.models.product import Product
from app.models.sub_category import SubCategory
from app.models.product_keys import ProductKeys
from app.models.user_products import UserProduct
from app.extensions import generate_password_hash


class DataBase:

    def __init__(self, db, app):
        self.db = db
        self.app = app

        self.db.init_app(self.app)

    def create_tables(self):
        with self.app.app_context():
            self.db.create_all()
            # check if exist admin user if not create admin user
            if not User.get_user_id(user_id=1):
                User.add_new_user(
                    username=os.environ.get('ADMIN_USER_EMAIL'),
                    password=generate_password_hash(password=os.environ.get('ADMIN_PASSWORD'), method='pbkdf2:sha256',
                                                    salt_length=8),
                    role='admin'
                )
