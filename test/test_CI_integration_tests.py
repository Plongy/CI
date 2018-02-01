""" Tests testing the endpoints of the server """
import pytest

import CI


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
