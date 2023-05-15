SHELL := /bin/bash

IMAGE_NAME := wallex/orchestrator
CONTAINER_NAME := orchestrator

build:
	docker build -t ${IMAGE_NAME} .

remove:
	docker rm -f ${CONTAINER_NAME}

run: remove
	docker run --name ${CONTAINER_NAME} -d ${IMAGE_NAME}

up:
	docker compose up -d

up-build:
	docker compose up --build -d

test: up
	docker compose exec app pytest -s

unit-test: up
	docker compose exec app pytest -s -m unit

integration-test: up
	docker compose exec app pytest -s -m integration

e2e-test: up
	docker compose exec app pytest -s -m e2e

this-test: up
	docker compose exec app pytest -s -m this

migrate: up
	docker compose exec app alembic upgrade head
