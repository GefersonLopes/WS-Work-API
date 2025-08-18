from sqlalchemy import Integer, String, DECIMAL, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ...extensions import db

class Model(db.Model):
    __tablename__ = "models"
    __table_args__ = (
        UniqueConstraint("nome", "marca_id", name="UQ_model_nome_brand"),
        Index("IDX_model_brand", "marca_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    brand_id: Mapped[int] = mapped_column("marca_id", Integer, ForeignKey("brands.id", ondelete="CASCADE"), nullable=False)
    nome: Mapped[str] = mapped_column(String(120), nullable=False)
    fipeValue: Mapped[float] = mapped_column("valor_fipe", DECIMAL(12, 2), nullable=False)

    brand = relationship("Brand", back_populates="models", cascade="all, delete", passive_deletes=True)
    cars  = relationship("Car", back_populates="model", cascade="all, delete", passive_deletes=True)
