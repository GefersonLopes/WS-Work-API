from sqlalchemy import Integer, String, Enum, CheckConstraint, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime
from ...extensions import db
import enum

class Fuel(str, enum.Enum):
    GASOLINA="GASOLINA"; ETANOL="ETANOL"; FLEX="FLEX"; DIESEL="DIESEL"; HIBRIDO="HIBRIDO"; ELETRICO="ELETRICO"

class Car(db.Model):
    __tablename__ = "cars"
    __table_args__ = (
        CheckConstraint('"num_portas" BETWEEN 2 AND 6', name='CHK_car_num_portas'),
        CheckConstraint('"ano" BETWEEN 1950 AND 2100', name='CHK_car_ano'),
        CheckConstraint('"combustivel" IN (\'GASOLINA\',\'ETANOL\',\'FLEX\',\'DIESEL\',\'HIBRIDO\',\'ELETRICO\')', name='CHK_car_combustivel'),
        Index("IDX_car_model", "modelo_id"),
        Index("IDX_car_createdAt", "timestamp_cadastro"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    createdAt: Mapped[str] = mapped_column("timestamp_cadastro", DateTime(timezone=True), nullable=False, server_default=db.func.now())
    model_id: Mapped[int] = mapped_column("modelo_id", Integer, ForeignKey("models.id", ondelete="RESTRICT"), nullable=False)

    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    combustivel: Mapped[Fuel] = mapped_column(Enum(Fuel, name="cars_combustivel_enum"), nullable=False)
    num_portas: Mapped[int] = mapped_column(Integer, nullable=False)
    cor: Mapped[str] = mapped_column(String(40), nullable=False)

    model = relationship("Model", back_populates="cars")
