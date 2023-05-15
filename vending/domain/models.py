from dataclasses import dataclass
from typing import Tuple, Dict

from .errors import InvalidState, ChoosingItemRequiresEnoughCoin, OutOfStock
from .valueobjects import State
from seedwork.domain import AggregateRoot


@dataclass
class Product:
    identifier: str
    name: str
    price: int


@dataclass
class Inventory:
    items: Dict[str, Tuple[Product, int]]

    def deduct(self, product: Product) -> None:
        product, stock = self.find(product.identifier)
        self.items[product.identifier] = (product, stock - 1)

    def find(self, identifier: str) -> Tuple[Product, int]:
        return self.items.get(identifier)


@dataclass
class Machine(AggregateRoot):
    identifier: str
    inventory: Inventory
    state: State
    cash_desk: int
    coin: int

    def cash_in(self, coin: int):
        self.coin = coin
        self.state = State.Choosing

    def choose(self, product_id: str):
        if self.state != State.Choosing:
            raise InvalidState.with_transform(self.state, State.Idle)

        product, stock = self.inventory.find(product_id)

        if product.price > self.coin:
            raise ChoosingItemRequiresEnoughCoin

        if stock < 1:
            raise OutOfStock.with_identifier(product_id)

        self.cash_desk += self.coin
        self.coin = 0
        self.state = State.Idle
        self.inventory.deduct(product)
