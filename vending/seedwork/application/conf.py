from .types import CommandConfig, QueryConfig, EventConfig

from application import commands, handlers
from infra.repo import RedisMachineRepo


Commands: CommandConfig = {
    commands.CashIn: (handlers.CashInHandler, RedisMachineRepo),
    commands.Choose: (handlers.ChooseHandler, RedisMachineRepo),
}

Events: EventConfig = {}

Queries: QueryConfig = {}
