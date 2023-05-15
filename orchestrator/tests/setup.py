import pathlib
from alembic.config import Config
from alembic import command


def alembic_config() -> Config:
    return Config(pathlib.Path(__file__).parent.parent / "alembic.ini")


def setup_function():
    command.upgrade(alembic_config(), 'head')


def teardown_function():
    command.downgrade(alembic_config(), 'base')
