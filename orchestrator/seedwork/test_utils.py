import pytest


def marks(*args):
    def _(f):
        for mark in args:
            f = getattr(pytest.mark, mark)(f)
        return f

    return _
