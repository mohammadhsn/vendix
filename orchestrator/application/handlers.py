from typing import Optional
from datetime import datetime

from seedwork.application.interfaces import CommandHandler
from .commands import RegisterMachine, SubmitPurchase
from domain.repo import MachineRepo, PurchaseRepo
from domain.models import Machine, Purchase
from .errors import InvalidMachineId


class RegisterMachineHandler(CommandHandler):
    def handle(self, command: RegisterMachine, repo: MachineRepo) -> Optional[str]:
        machine = Machine(identifier=repo.next_identity(), hardware_id=command.hardware_id)
        repo.persist(machine)
        return machine.identifier


class SubmitPurchaseHandler(CommandHandler):
    def __init__(self, machines: MachineRepo):
        self.machines = machines

    def handle(self, command: SubmitPurchase, repo: Optional[PurchaseRepo]) -> Optional[str]:
        if self.machines.find_by_id(command.machine_id) is None:
            raise InvalidMachineId.from_identifier(command.machine_id)

        purchase = Purchase(repo.next_identity(), command.machine_id, command.product_id,
                            command.price, datetime.now())
        repo.persist(purchase)
        return purchase.identifier
