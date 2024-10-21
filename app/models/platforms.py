from app.extensions import *

class Platform(db.Model):
    __tablename__ = 'platforms'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)

    def __repr__(self):
        return f'<Platform "{self.name}">'