from app.extensions import *

class UserProduct(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id:Mapped[int] = mapped_column(Integer, ForeignKey('products.id'), nullable=False)
    key_id: Mapped[int] = mapped_column(Integer, ForeignKey('keys.id'), nullable=False)