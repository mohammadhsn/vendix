from domain.repo import MachineRepo
from infra.repo import redis_client

from seedwork.test_utils import marks

from .fixtures import idle_machine, inventory, soda, coffee, repo # noqa
from domain.valueobjects import State


def teardown_function():
    redis_client().flushall()


@marks('integration')
def test_persist(idle_machine, repo: MachineRepo):
    coffee, coffe_stock = idle_machine.inventory.find('coffee')
    idle_machine.cash_in(coffee.price)
    repo.persist(idle_machine)
    fetched = repo.fetch()
    assert fetched.state == State.Choosing
    assert fetched.coin == coffee.price
    idle_machine.choose(coffee.identifier)
    repo.persist(idle_machine)
    fetched = repo.fetch()
    assert fetched.cash_desk == coffee.price
