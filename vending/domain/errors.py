from .valueobjects import State
from seedwork.domain import DomainError


class OutOfStock(DomainError):
    @classmethod
    def with_identifier(cls, product_id: str) -> 'OutOfStock':
        return cls("%s is out of stack and cannot be ordered" % product_id)


class ChoosingItemRequiresEnoughCoin(DomainError):
    pass


class InvalidState(DomainError):
    @classmethod
    def with_transform(cls, a, b: State):
        return cls("cannot transform from state %s, to %s" % (a, b))
