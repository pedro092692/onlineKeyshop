from app.models.post import Post
from app.models.user import User
from app.models.platforms import Platform
from app.models.category import Category

class DataBase:

    def __init__(self, db, app):
        self.db = db
        self.app = app

        self.db.init_app(self.app)

    def create_tables(self):
        with self.app.app_context():
            self.db.create_all()