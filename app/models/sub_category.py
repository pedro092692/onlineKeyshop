from sqlalchemy.orm import relationship

from app.extensions import *

class SubCategory(db.Model):

    __tablename__ = "sub_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    category: Mapped["categories"] = relationship(cascade="all, delete-orphan")