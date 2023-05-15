from dataclasses import dataclass
from seedwork.application.interfaces import Command


@dataclass
class RegisterMachine(Command):
    hardware_id: str


@dataclass
class SubmitPurchase(Command):
    machine_id: str
    product_id: str
    price: int
