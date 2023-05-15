import pytest
from seedwork.test_utils import marks
from adapters.flask.app import app as flask_app
from flask import Flask
from flask.testing import FlaskClient
from .setup import setup_function, teardown_function # noqa


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
def test_register_new_machine(client: FlaskClient):
    res = client.post('/register', json={'hardware_id': 'foo'})
    assert res.status_code == 201
    assert 'id' in res.json.keys()


@marks('e2e')
def test_submit_a_purchase(client: FlaskClient):
    # register a machine first
    machine_id = client.post('/register', json={'hardware_id': 'foo'}).json['id']

    res = client.post('/purchase', json={'machine': machine_id, 'product': 'coffee', 'price': 5})
    assert res.status_code == 201
    assert 'id' in res.json.keys()
