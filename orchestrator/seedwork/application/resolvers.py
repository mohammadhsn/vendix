from application.handlers import SubmitPurchaseHandler
from infra.orm.repo import PostgresMachineRepo


def resolve_purchase_handler() -> SubmitPurchaseHandler:
    return SubmitPurchaseHandler(PostgresMachineRepo())
