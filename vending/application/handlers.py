from typing import Optional

from seedwork.application.interfaces import CommandHandler
from domain.repo import MachineRepo

from .commands import CashIn, Choose


class CashInHandler(CommandHandler):
    def handle(self, command: CashIn, repo: MachineRepo) -> Optional[str]:
        machine = repo.fetch()
        machine.cash_in(command.coin)
        repo.persist(machine)
        return None


class ChooseHandler(CommandHandler):
    def handle(self, command: Choose, repo: MachineRepo) -> Optional[str]:
        machine = repo.fetch()
        machine.choose(command.product_id)
        repo.persist(machine)
        return None
