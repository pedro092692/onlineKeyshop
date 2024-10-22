from app.models.post import Post
from app.models.user import User
from app.models.platforms import Platform
from app.models.key import Key
from app.models.category import Category
from app.models.product import Product
from app.models.sub_category import SubCategory
from app.models.product_keys import ProductKeys

class DataBase:

    def __init__(self, db, app):
        self.db = db
        self.app = app

        self.db.init_app(self.app)

    def create_tables(self):
        with self.app.app_context():
            self.db.create_all()