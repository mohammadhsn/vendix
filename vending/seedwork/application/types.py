from typing import Mapping, Type, Tuple, Iterable, Dict, Union, List
from .interfaces import Command, CommandHandler, Listener, Query, QueryHandler
from ..domain import Repository, DomainEvent

CommandConfig = Mapping[Type[Command], Tuple[Type[CommandHandler], Type[Repository]]]

QueryConfig = Mapping[Type[Query], Type[QueryHandler]]

EventConfig = Mapping[
    Type[DomainEvent], Iterable[Tuple[Type[Listener], Type[Repository]]]
]

"""
events = {
    SomethingHappened: [
        (someContext.TheListener, TheRepo),
        (someOtherContext.TheListener, anOtherRepo),
    ]
}
"""
