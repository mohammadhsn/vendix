from .models import Machine
from seedwork.domain import Repository


class MachineRepo(Repository):
    def fetch(self) -> Machine:
        raise NotImplementedError

    def persist(self, machine: Machine) -> None:
        raise NotImplementedError
