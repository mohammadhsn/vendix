import pytest
from seedwork.test_utils import marks
from adapters.flask.app import app as flask_app
from flask import Flask
from infra.repo import redis_client
from flask.testing import FlaskClient
from domain.models import Machine, Inventory, Product
from .fixtures import idle_machine, inventory, soda, coffee, repo # noqa
from domain.repo import MachineRepo


def teardown_function():
    redis_client().flushall()


@pytest.fixture
def app() -> Flask:
    flask_app.config.update({
        "TESTING": True,
    })

    yield flask_app


@pytest.fixture()
def client(app) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@marks('e2e')
def test_cash_in(client: FlaskClient):
    response = client.post("/cash-in", json={
        'cash': 2
    })
    assert response.status_code == 204


@marks('e2e')
def test_choose(client: FlaskClient, idle_machine: Machine, repo: MachineRepo, coffee: Product):
    # make the coffee product available
    idle_machine.inventory = Inventory({
        coffee.identifier: (coffee, 1)
    })
    repo.persist(idle_machine)

    # do the cash-in job
    client.post('/cash-in', json={'cash': coffee.price})
    # purchase the coffee
    res = client.post('/choose', json={'product_id': coffee.identifier})
    assert res.status_code == 204
