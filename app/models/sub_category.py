from sqlalchemy.orm import relationship
from app.extensions import *
from app.models.product import Product
from app.models.product_keys import ProductKeys
from app.models.helpers import add_item


class SubCategory(db.Model):

    __tablename__ = "sub_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped["Category"] = relationship()
    products: Mapped["Product"] = relationship(back_populates="sub_category")

    @staticmethod
    def get_subcategories():
        subquery = exists().where(
            ProductKeys.product_id == Product.id,
            ProductKeys.key_id != None
            )

        subcategories = (
            db.session.query(SubCategory)
            .join(Product)
            .filter(subquery)
            .order_by(SubCategory.id.desc())
            .all()
        )

        return subcategories

    @staticmethod
    def add_subcategory(model, *args):
        return add_item(model, *args)
