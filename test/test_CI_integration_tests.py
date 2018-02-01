""" Tests testing the endpoints of the server """
import pytest

import CI
from CI.CI_helpers import *


@pytest.fixture
def app():
    return CI.app


@pytest.fixture
def client():
    app.testing = True
    return CI.app.test_client()


def test_index(client):
    # Test that index returns a response saying "Hello, World!"
    res = client.get('/')
    assert res.status_code == 200
    assert b'Hello, World!' == res.data


def test_run_commands_positive():
    commands = ["echo hello", "echo bye"]
    command_output = run_commands(commands)
    assert command_output == [b'hello\n', b'bye\n']


def test_run_commands_negative():
    """ First command is invalid, will throw an exception and 'Error' is appended
    to list """
    commands = ["ech hello", "echo hello"]
    command_output = run_commands(commands)
    assert command_output == ["Error", b'hello\n']
