from sqlalchemy.orm import relationship
from app.extensions import *
from app.models.product import Product
from app.models.product_keys import ProductKeys
from app.models.helpers import add_item


class Platform(db.Model):
    __tablename__ = 'platforms'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    products: Mapped[List["Product"]] = relationship(back_populates="platform")

    def __repr__(self):
        return f'<Platform "{self.name}">'

    @staticmethod
    def get_platforms():
        subquery = exists().where(
            ProductKeys.product_id == Product.id,
            ProductKeys.key_id != None
        )
        platforms = (
            db.session.query(Platform)
            .join(Product)
            .filter(subquery)
            .order_by(Platform.id.desc())
            .all()
        )
        return platforms

    @staticmethod
    def add_platform(model, *args):
        return add_item(model, *args)
