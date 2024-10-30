from sqlalchemy.orm import relationship
from app.extensions import *
from app.models.product import Product
from app.models.product_keys import ProductKeys
from app.models.helpers import add_item, search_item, get_item, update_item, delete_item


class Platform(db.Model):
    __tablename__ = 'platforms'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    products: Mapped[List["Product"]] = relationship(back_populates="platform", cascade="all,delete")

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

    @staticmethod
    def platforms_paginate():
        platforms = db.paginate(db.select(Platform).order_by(Platform.id.desc()), per_page=8)
        return platforms

    @staticmethod
    def platforms():
        all_platforms = db.session.execute(db.select(Platform).order_by(Platform.id.asc())).scalars().all()
        return all_platforms

    @staticmethod
    def get_platform(platform_id):
        return get_item(Platform, platform_id)

    @staticmethod
    def search_platform(query):
        return search_item(query, Platform)

    @staticmethod
    def update_platform(platform, *args):
        return update_item(platform, *args)

    @staticmethod
    def delete_platform(platform):
        return delete_item(platform)
