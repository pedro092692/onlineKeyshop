from app.extensions import db
from app.extensions import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User "{self.username}">'

    @staticmethod
    def find_user(email):
        query = db.session.query(User).filter_by(username=email)
        user = db.session.execute(query).scalar()
        return user

    @staticmethod
    def add_new_user(username, password):
        new_user = User(
            username=username,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()

    @staticmethod
    def get_user_id(user_id):
        user = db.get_or_404(User, user_id)
        return user

