from typing import List, Optional
from types import MappingProxyType
import pytest
from unittest.mock import patch
from seedwork.application.interfaces import (
    Command,
    Query,
    CommandHandler,
    QueryHandler,
    Listener,
)
from seedwork.application.bus import InMemoryBus, InMemoryQueryBus
from seedwork.application.types import CommandConfig, EventConfig, QueryConfig
from seedwork.domain import AggregateRoot, DomainEvent, Repository


class SomethingHappened(DomainEvent):
    pass


class SomethingElseHappened(DomainEvent):
    pass


class DummyAggregate(AggregateRoot):
    def some_something(self):
        self._record(SomethingHappened())


class DummyRepository(Repository):
    def __init__(self):
        self._seen: List[AggregateRoot] = []

    def seen(self) -> List[AggregateRoot]:
        return self._seen

    def add(self, agg: DummyAggregate):
        self._seen.append(agg)


class DoSomething(Command):
    pass


_handler_calls = 0


class DoSomethingListener(Listener):
    def handle(self, event: SomethingHappened, repo: DummyRepository) -> None:
        pass


class DoSomethingHandler(CommandHandler):
    def __init__(self):
        self.call_count = 0

    def handle(self, command: Command, repo: DummyRepository) -> Optional[str]:
        agg = DummyAggregate()
        agg.some_something()
        repo.add(agg)
        global _handler_calls
        _handler_calls += 1
        return None


class TestBus:
    COMMANDS: CommandConfig = MappingProxyType(
        {DoSomething: (DoSomethingHandler, DummyRepository)}
    )
    EVENTS: EventConfig = MappingProxyType(
        {
            SomethingHappened: [
                (
                    DoSomethingListener,
                    DummyRepository,
                )
            ]
        }
    )

    @pytest.fixture
    def bus(self) -> InMemoryBus:
        return InMemoryBus(self.COMMANDS, self.EVENTS)

    def test_handling_a_command(self, bus: InMemoryBus):
        bus.handle(DoSomething())
        assert 1 == _handler_calls

    def test_handling_commands_lead_to_publish_events(self):
        repo = DummyRepository()
        DoSomethingHandler().handle(DoSomething(), repo)
        assert 1 == len(repo.seen())
        assert isinstance(repo.seen()[0].pull_recorded_events()[0], SomethingHappened)

    def test_bus_continues_execution_until_events_exist(self, bus: InMemoryBus):
        listener = DoSomethingListener()
        with patch.object(DoSomethingListener, "handle", wraps=listener.handle) as mock:
            bus.handle(DoSomething())
            mock.assert_called_once()


class SomeQuery(Query):
    def __init__(self, some_filter: str):
        self.some_filter = some_filter


class SomeQueryHandler(QueryHandler):
    def handle(self, query: SomeQuery):
        return {"foo": "bar"}


class TestQueryBus:
    QUERIES: QueryConfig = {SomeQuery: SomeQueryHandler}

    def test_handle_query(self):
        bus = InMemoryQueryBus(self.QUERIES)

        assert {"foo": "bar"} == bus.ask(SomeQuery("foo"))
