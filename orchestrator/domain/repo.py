from abc import ABCMeta
from typing import Optional

from seedwork.domain import Repository
from .models import Machine, Purchase


class MachineRepo(Repository):
    def persist(self, machine: Machine):
        raise NotImplementedError

    def find_by_id(self, identifier: str) -> Optional[Machine]:
        raise NotImplementedError

    def next_identity(self) -> str:
        raise NotImplementedError


class PurchaseRepo(Repository):
    def persist(self, purchase: Purchase):
        raise NotImplementedError

    def next_identity(self) -> str:
        raise NotImplementedError
