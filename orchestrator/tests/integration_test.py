import uuid
import pytest
from datetime import datetime
from domain.models import Machine, Purchase
from domain.repo import MachineRepo, PurchaseRepo
from infra.orm.repo import PostgresMachineRepo, PostgresPurchaseRepo
from infra.orm.models import SqlalchemyMachine, SqlalchemyPurchase
from infra.orm.connection import engine
from seedwork.test_utils import marks
from .setup import setup_function, teardown_function # noqa

from sqlalchemy import select
from sqlalchemy.orm import Session


@pytest.fixture
def machine_repo() -> MachineRepo:
    return PostgresMachineRepo()


@pytest.fixture
def purchase_repo() -> PurchaseRepo:
    return PostgresPurchaseRepo()


@marks('integration')
def test_persist_machine(machine_repo: MachineRepo):
    machine = Machine(machine_repo.next_identity(), 'hw-foo')
    machine_repo.persist(machine)
    with Session(engine) as session:
        fetched: SqlalchemyMachine = session.scalar(
            select(SqlalchemyMachine).where(SqlalchemyMachine.id == machine.identifier))
        assert machine.identifier == fetched.id
        assert machine.hardware_id == fetched.hardware_id


@marks('integration')
def test_persist_purchase(purchase_repo: PurchaseRepo):
    purchase = Purchase(purchase_repo.next_identity(), str(uuid.uuid4()), 'coffee', 4, datetime.now())
    purchase_repo.persist(purchase)
    with Session(engine) as session:
        fetched: SqlalchemyPurchase = session.scalar(
            select(SqlalchemyPurchase).where(SqlalchemyPurchase.id == purchase.identifier))

    assert fetched.id == purchase.identifier
    assert fetched.machine_id == purchase.machine_id
    assert fetched.product_id == purchase.product_id
    assert fetched.price == purchase.price
    assert fetched.at == purchase.at
