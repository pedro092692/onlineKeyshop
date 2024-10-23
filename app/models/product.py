from sqlalchemy.orm import relationship
from app.extensions import *
from app.models.category import Category
from app.models.platforms import Platform
from app.models.product_keys import ProductKeys
from app.models.sub_category import SubCategory


class Product(db.Model):

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    platform_id: Mapped[int] = mapped_column(Integer, ForeignKey("platforms.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    sub_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("sub_categories.id", ondelete="CASCADE"))
    product_keys: Mapped[List["ProductKeys"]] = relationship(back_populates="product_info")
    category: Mapped["Category"] = relationship()
    sub_category: Mapped["SubCategory"] = relationship()
    platform: Mapped["Platform"] = relationship()

    @staticmethod
    def get_products():
        all_products = db.session.execute(db.select(Product).order_by(Product.name)).scalars().all()
        return all_products
