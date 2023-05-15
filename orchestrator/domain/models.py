from dataclasses import dataclass
from datetime import datetime


@dataclass
class Machine:
    identifier: str
    hardware_id: str


@dataclass
class Product:
    pass


@dataclass
class Purchase:
    identifier: str
    machine_id: str
    product_id: str
    price: int
    at: datetime
