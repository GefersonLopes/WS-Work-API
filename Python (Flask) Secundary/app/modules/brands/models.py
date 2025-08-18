from sqlalchemy import Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...extensions import db

class Brand(db.Model):
    __tablename__ = "brands"
    __table_args__ = (UniqueConstraint("nome_marca", name="UQ_brand_nome"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column("nome_marca", String(120), nullable=False)

    models = relationship("Model", back_populates="brand", cascade="all, delete", passive_deletes=True)
