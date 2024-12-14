from app.extensions import db
from app.extensions import UserMixin
from app.models.helpers import add_item

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __repr__(self):
        return f'<User "{self.username}">'

    @staticmethod
    def find_user(email):
        query = db.session.query(User).filter_by(username=email)
        user = db.session.execute(query).scalar()
        return user

    @staticmethod
    def add_new_user(*args):
        return add_item(User, *args)

    @staticmethod
    def get_user_id(user_id):
        user = db.session.execute(db.select(User).filter(User.id == user_id)).scalar()
        return user
