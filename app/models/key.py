from app.extensions import *

class Key(db.Model):
    __tablename__ = 'keys'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key_value: Mapped[str] = mapped_column(String(250), primary_key=True)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<Key "{self.key_value}">'