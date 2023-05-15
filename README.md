# Vendix

An integrated vending machine management system

## Disclaim
*This code is just for explaining system/software design opinions, and it's not proper for running on production*

## System design
The software is composed of two services:
**Vending**: 
It's going to be deployed for each physical vending machine.
It uses Python and Redis to work and keep the machine state
**Orchestrator**: A centralized deployable unit for managing vending machines.
It uses Python and Postgres to keep track of vending machines.

## Scenario
- Deploy the `orchestrator` service somewhere in a highly available way [using its docker image](https://github.com/mohammadhsn/vendix/blob/main/orchestrator/Dockerfile).
- Deploy an instance of the `vending` service or each new physical vending machine [using the docker image]([https://github.com/mohammadhsn/orchestrator/blob/main/orchestrator/Dockerfile](https://github.com/mohammadhsn/vendix/blob/main/orchestrator/Dockerfile)).
- Register the machine using the `/register` API
- Define products on each vending

## Architectural patterns
Each service uses a clean/hexagonal architecture with four main parts: `domain,` `application,` `infrastructure,` and `adapters.` The domain layers use the DDD building blocks such as aggregates, value objects, etc.

## A use case development journey
- Create or modify pure domain objects and cover them with unit tests. It supposes not to involve any kind of infrastructure thing like a database
- Create Application level behavior, including command/handler. The application layer handlers use repository interfaces to ship data which is decoupled from the data technology
- Create infrastructure requirements (like db) and cover it with integration testing
- Create an adapter (like HTTP rest) and cover it with end-to-end testing


## Improvements
These two services need to be connected using a reliable approach way of communication. An AMQP approach with applied [outbox pattern](https://microservices.io/patterns/data/transactional-outbox.html) can be good.
