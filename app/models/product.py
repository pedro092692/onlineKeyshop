from sqlalchemy.orm import relationship

from app.extensions import *

class Product(db.Model):

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    platform_id: Mapped[int] = mapped_column(Integer, ForeignKey("platforms.id"))
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    product_keys: Mapped[List["product_keys"]] = relationship(back_populates="product_info")