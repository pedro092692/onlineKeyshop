from sqlalchemy.orm import relationship
from app.models.key import Key
from app.models.helpers import add_item
from app.extensions import *

class ProductKeys(db.Model):

    __tablename__ = "product_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    key_id: Mapped[int] = mapped_column(Integer, ForeignKey("keys.id", ondelete="CASCADE"))
    product_info: Mapped["Product"] = relationship(back_populates="product_keys")
    key_info: Mapped["Key"] = relationship()

    @staticmethod
    def add_new_product_key(model, *args):
        return add_item(model, *args)