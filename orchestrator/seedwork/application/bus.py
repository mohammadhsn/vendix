from typing import Union, List

from seedwork.domain import DomainEvent

from .types import CommandConfig, EventConfig, QueryConfig

from .interfaces import Command, Query, Bus, QueryBus

from .conf import Commands, Queries, Events


class InMemoryBus(Bus):
    def __init__(self, commands: CommandConfig, events: EventConfig):
        self.commands = commands
        self.events = events
        self.queue: List[DomainEvent] = []
        self.output = None

    def handle(self, message: Union[Command | DomainEvent]) -> Union[str, None]:
        return self._perform_handle(message)

    def _perform_handle(
        self, message: Union[Command | DomainEvent]
    ) -> Union[str, None]:
        if isinstance(message, Command):
            self._handle_command(message)
        elif isinstance(message, DomainEvent):
            self._handle_event(message)
        else:
            raise

        while self.queue:
            self._perform_handle(self.queue.pop())

        return self.output

    def _handle_command(self, command: Command):
        handler, repo = self.commands[command.__class__]
        self.output = handler().handle(command, repo := repo())
        for aggregate in repo.seen():
            self.queue.extend(aggregate.pull_recorded_events())

    def _handle_event(self, event: DomainEvent):
        for listener_class, repo_class in self.events.get(event.__class__, []):
            listener_class().handle(event, repo := repo_class())
            for aggregate in repo.seen():
                self.queue.extend(aggregate.pull_recorded_events())


class InMemoryQueryBus(QueryBus):
    def __init__(self, queries: QueryConfig):
        self.queries = queries

    def ask(self, query: Query):
        if query.__class__ not in self.queries:
            raise

        return self.queries[query.__class__]().handle(query)


bus = InMemoryBus(Commands, Events)

query_bus = InMemoryQueryBus(Queries)
