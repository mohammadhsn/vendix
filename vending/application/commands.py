from dataclasses import dataclass
from seedwork.application.interfaces import Command


@dataclass
class CashIn(Command):
    coin: int


@dataclass
class Choose(Command):
    product_id: str
