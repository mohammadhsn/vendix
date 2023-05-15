import pytest

from domain.models import Product, Inventory, Machine
from domain.repo import MachineRepo
from domain.valueobjects import State
from infra.repo import RedisMachineRepo

COFFEE_PRICE: int = 5
SODA_PRICE: int = 8


@pytest.fixture
def soda() -> Product:
    return Product(identifier="soda", name="Soda", price=SODA_PRICE)


@pytest.fixture
def coffee() -> Product:
    return Product(identifier="coffee", name="Coffee", price=COFFEE_PRICE)


@pytest.fixture
def inventory(soda, coffee: Product) -> Inventory:
    return Inventory(
        {
            soda.identifier: (soda, 3),
            coffee.identifier: (coffee, 2),
        }
    )


@pytest.fixture
def out_stock_coffe(soda, coffee: Product) -> Inventory:
    return Inventory(
        {
            soda.identifier: (soda, 3),
            coffee.identifier: (coffee, 0),
        }
    )


@pytest.fixture
def idle_machine(inventory: Inventory) -> Machine:
    return Machine(
        identifier="foo", inventory=inventory, state=State.Idle, cash_desk=0, coin=0
    )


@pytest.fixture
def repo() -> MachineRepo:
    return RedisMachineRepo()
