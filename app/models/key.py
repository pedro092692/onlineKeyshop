from sqlalchemy import Float
from app.models.helpers import add_item
from app.extensions import *

class Key(db.Model):
    __tablename__ = 'keys'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key_value: Mapped[str] = mapped_column(String(250), nullable=False)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)


    def __repr__(self):
        return f'<Key "{self.key_value}">'

    @staticmethod
    def add_key(model, *args):
        return add_item(model, *args)