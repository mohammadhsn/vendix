import uuid
from typing import Optional, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.models import Machine, Purchase
from domain.repo import MachineRepo, PurchaseRepo
from seedwork.domain import AggregateRoot

from .connection import engine
from .models import SqlalchemyMachine, SqlalchemyPurchase


class PostgresMachineRepo(MachineRepo):
    def __init__(self):
        self.session = Session(engine)

    def persist(self, machine: Machine):
        with self.session as session:
            m = SqlalchemyMachine(id=machine.identifier, hardware_id=machine.hardware_id)
            session.add(m)
            session.commit()

    def find_by_id(self, identifier: str) -> Optional[Machine]:
        with self.session as session:
            fetched: SqlalchemyMachine = session.scalar(
                select(SqlalchemyMachine).where(SqlalchemyMachine.id == identifier))

        return fetched.to_domain() if fetched else None

    def next_identity(self) -> str:
        return str(uuid.uuid4())

    def seen(self) -> List[AggregateRoot]:
        return []


class PostgresPurchaseRepo(PurchaseRepo):
    def __init__(self):
        self.session = Session(engine)

    def persist(self, purchase: Purchase):
        with self.session as session:
            p = SqlalchemyPurchase(id=purchase.identifier, machine_id=purchase.machine_id,
                                   product_id=purchase.product_id,
                                   price=purchase.price, at=purchase.at)

            session.add(p)
            session.commit()

    def next_identity(self) -> str:
        return str(uuid.uuid4())

    def seen(self) -> List[AggregateRoot]:
        return []
