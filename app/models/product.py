from sqlalchemy.orm import relationship
from app.extensions import *
from app.models.helpers import add_item, get_item, update_item, delete_item


class Product(db.Model):

    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    platform_id: Mapped[int] = mapped_column(Integer, ForeignKey("platforms.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    sub_category_id: Mapped[int] = mapped_column(Integer, ForeignKey("sub_categories.id", ondelete="CASCADE"))
    product_keys: Mapped[List["ProductKeys"]] = relationship(back_populates="product_info", cascade="all,delete")
    category: Mapped["Category"] = relationship()
    sub_category: Mapped["SubCategory"] = relationship(back_populates="products")
    platform: Mapped["Platform"] = relationship(back_populates="products")

    @staticmethod
    def get_products():
        all_products = db.paginate(db.select(Product).order_by(Product.id.desc()), per_page=8)
        return all_products

    @staticmethod
    def latest_products():
        latest_product = (
            db.session.query(Product)
            .filter_by(category_id=1)
            .join(Product.product_keys)
            .order_by(Product.id.desc())
            .limit(5)
            .all()
        )
        return latest_product

    @staticmethod
    def get_latest_gift_cards():
        latest_gift_cards = (
            db.session.query(Product)
            .filter(Product.category_id == 2)
            .join(Product.product_keys)
            .order_by(Product.id.desc())
            .limit(5)
            .all()
        )
        return latest_gift_cards

    @staticmethod
    def add_product(model, *args):
        return add_item(model, *args)

    @staticmethod
    def get_product(product_id):
        return get_item(Product, product_id)

    @staticmethod
    def update_product(product, *args):
        return update_item(product, *args)

    @staticmethod
    def delete_product(product):
        return delete_item(product)


    @staticmethod
    def search_product(query):
        from app.models.platforms import Platform
        products = db.paginate(db.select(Product).join(Product.platform).filter(
            Product.name.icontains(query) | Platform.name.icontains(query)
        ).order_by(Product.name), per_page=8)

        return products



