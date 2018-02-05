""" Tests testing the endpoints of the server """
import os
from unittest.mock import mock_open, patch, MagicMock, Mock

import pytest

import CI
from CI import constants


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


def test_github_webhook(client):
    # Contract: function runs commands in the correct folder and the whole process seems to work
    # Does not test repo cloning and that build state is set on github

    root_dir = os.getcwd()
    repo_name = "foo/bar"
    sha = "f00ba2"

    # Mocked config file
    conf = mock_open(read_data=f"""{{
                    "commands": ["pwd", "echo foo bar"],
                    "success_strings": ["{root_dir}/{constants.CLONE_FOLDER}{repo_name}/{sha}", "fo+ bar"]
                  }}""")

    # Webhook post data
    webhook_data = f"""{{
        "ref":"ref/heads/not_master",
        "head_commit": {{
            "id": "{sha}"
        }},
        "repository": {{
            "ssh_url": "invalid",
            "full_name": "{repo_name}"
        }}
    }}"""

    # Mocked clone function that just creates the target folder
    fake_clone = Mock(side_effect=lambda x, y, z: os.mkdir(z))

    fake_set_state = MagicMock()

    fake_log_process = MagicMock()

    with patch('CI.CI_helpers.open', conf):
        with patch('CI.routes.clone_repo', fake_clone) as patch_clone:
            with patch('CI.routes.set_commit_state', fake_set_state) as patch_set_state:
                with patch('CI.routes.log_process', fake_log_process):
                    client.post('/hooks/github', data=webhook_data, content_type='application/json')

    conf.assert_called_once_with(f"{constants.CLONE_FOLDER}{repo_name}/{sha}/{constants.CONF}")
    patch_clone.assert_called_with("invalid", "not_master", f"{constants.CLONE_FOLDER}{repo_name}/{sha}")

    assert patch_set_state.call_count == 2
    patch_set_state.assert_any_call(repo_name, sha, "pending")
    patch_set_state.assert_called_with(repo_name, sha, "success")

    fake_log_process.assert_called_once()


def test_build_info(client):
    m = mock_open(
        read_data='{"date": "170623","hash": "007","results": ['
                  '{"command": "echo hello","status": 0,"output": "hello\\n"},'
                  '{"command": "echo bye","status": 0,"output": "bye\\n"}'
                  ']}'
    )
    owner_name = "owner"
    repo_name = "repo"
    build_id = "1"

    with patch('CI.routes.open', m):
        res = client.get('/history/' + owner_name + '/' + repo_name + '/' + build_id)

    m.assert_called_once_with(f"{constants.HISTORY_FOLDER}{owner_name}/{repo_name}/{build_id}.json")

    assert res.status_code == 200
