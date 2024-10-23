from app.extensions import *
from app.models.product import Product
from app.models.product_keys import ProductKeys


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)


    @staticmethod
    def get_categories():
        subquery = exists().where(
            ProductKeys.product_id == Product.id,
            ProductKeys.key_id != None
        )
        categories = (
            db.session.query(Category)
            .join(Product)
            .filter(subquery)
            .order_by(Category.id.desc())
            .all()
        )
        return categories