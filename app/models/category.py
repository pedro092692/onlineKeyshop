from app.extensions import *
from app.models.product import Product
from app.models.product_keys import ProductKeys
from app.models.helpers import add_item, search_item, get_item, update_item, delete_item


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

    @staticmethod
    def categories():
        categories = db.paginate(db.select(Category).order_by(Category.id.asc()), per_page=8)
        return categories


    @staticmethod
    def add_category(model, *args):
        return add_item(model, *args)

    @staticmethod
    def search_category(query):
        return search_item(query, Category)

    @staticmethod
    def get_category(category_id):
        return get_item(Category, category_id)

    @staticmethod
    def update_category(category, *args):
        return update_item(category, *args)

    @staticmethod
    def delete_category(category):
        return delete_item(category)
