from .types import CommandConfig, QueryConfig, EventConfig

from application import commands, handlers
from infra.orm import repo
from . import resolvers


Commands: CommandConfig = {
    commands.RegisterMachine: (handlers.RegisterMachineHandler, repo.PostgresMachineRepo),
    commands.SubmitPurchase: (resolvers.resolve_purchase_handler, repo.PostgresPurchaseRepo),
}

Events: EventConfig = {}

Queries: QueryConfig = {}
