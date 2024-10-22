from sqlalchemy.orm import relationship

from app.extensions import *

class ProductKeys(db.Model):

    __tablename__ = "product_keys"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    key_id: Mapped[int] = mapped_column(Integer, ForeignKey("keys.id"))
    product_info: Mapped["products"] = relationship(back_populates="product_keys")