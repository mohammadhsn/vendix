# Vending service

You need to docker compose to up and running for local development.

## build docker image
```sh
make build
```


## up and running everything
```sh
make up
```

## running tests
```sh
make test
```
only units:
```sh
make unit-test
```
only integration:
```sh
make integration-test
```
only end to end tests:
```sh
make e2e-test
```
