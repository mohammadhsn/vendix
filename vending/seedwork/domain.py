from typing import List


class DomainEvent:
    pass


class AggregateRoot:
    def __init__(self):
        self._events: List[DomainEvent] = []

    def _record(self, event: DomainEvent) -> None:
        self._events.append(event)

    def pull_recorded_events(self) -> List[DomainEvent]:
        events = self._events[:]
        self._events = []
        return events


class Repository:
    def seen(self) -> List[AggregateRoot]:
        raise NotImplementedError


class DomainError(RuntimeError):
    pass
