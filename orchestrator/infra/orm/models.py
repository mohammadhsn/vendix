from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from domain.models import Machine as MachineDomainModel


class Base(DeclarativeBase):
    pass


class SqlalchemyMachine(Base):
    __tablename__ = "machines"

    id: Mapped[str] = mapped_column(primary_key=True)
    hardware_id: Mapped[str] = mapped_column()

    def to_domain(self) -> MachineDomainModel:
        return MachineDomainModel(self.id, self.hardware_id)

    def __repr__(self) -> str:
        return f"Machine(id={self.id!r}, hardware_id={self.hardware_id!r}"


class SqlalchemyPurchase(Base):
    __tablename__ = "purchases"

    id: Mapped[str] = mapped_column(primary_key=True)
    machine_id: Mapped[str] = mapped_column()
    product_id: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    at: Mapped[datetime] = mapped_column()
