from typing import List

from domain.models import Machine, Product, Inventory
from domain.repo import MachineRepo
from domain.valueobjects import State
from .redis import redis_client
from seedwork.domain import AggregateRoot


class RedisMachineRepo(MachineRepo):
    products = (
        Product('coffee', 'A Hot Coffee', 5),
        Product('soda', 'A Cold Soda', 8),
    )

    def __init__(self, redis=None):
        self.redis = redis or redis_client()

    def fetch(self) -> Machine:
        items = {
            p.identifier: (p, self._get_stock(p.identifier))
            for p in self.products
        }

        return Machine(identifier="foo",
                       inventory=Inventory(items),
                       state=self._get_state(),
                       cash_desk=self._get_desk_cash(),
                       coin=self._get_cash())

    def persist(self, machine: Machine) -> None:
        self._set_state(machine.state)
        self._set_desk_cash(machine.cash_desk)
        self._set_cash(machine.coin)

        for product, stock in machine.inventory.items.values():
            self._set_stock(product.identifier, stock)

    def seen(self) -> List[AggregateRoot]:
        return []

    def _get_desk_cash(self, default: int = 0) -> int:
        if persisted_cash := self.redis.get('desk_cash'):
            return int(persisted_cash)
        return default

    def _set_desk_cash(self, cash: int) -> None:
        self.redis.set('desk_cash', cash)

    def _get_state(self, default: State = State.Idle) -> State:
        if persisted_state := self.redis.get('state'):
            return State(int(persisted_state))
        return default

    def _set_state(self, state: State) -> None:
        self.redis.set('state', state.value)

    def _get_cash(self, default: int = 0) -> int:
        if persisted_coin := self.redis.get('cash'):
            return int(persisted_coin)
        return default

    def _set_cash(self, cash: int) -> None:
        self.redis.set('cash', cash)

    def _set_stock(self, product_id: str, stock: int) -> None:
        self.redis.set(f'stock:{product_id}', stock)

    def _get_stock(self, product_id: str, default=0) -> int:
        if exist := self.redis.get(f'stock:{product_id}'):
            return int(exist)

        return default
