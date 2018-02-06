import os
import shutil
import subprocess
from unittest.mock import mock_open, patch

import requests_mock

from CI import constants
from CI.CI_helpers import run_commands, clone_repo, is_successful_command, read_configfile, set_commit_state


def test_run_commands_positive():
    """Contract: run_commands() executes the commands provided in it's parameters"""
    commands = ["echo hello", "echo bye"]
    command_output = run_commands(commands)
    assert command_output == ['hello\n', 'bye\n']


def test_run_commands_negative():
    """Contract: If the first command is invalid, will throw an exception and 'Error' is appended
    to list """
    commands = ["ech hello", "echo hello"]
    command_output = run_commands(commands)
    assert command_output == ["Error", 'hello\n']


def test_clone_repo():
    """ Contract: Will return false since we are trying to clone a non-existing repo"""
    assert clone_repo("fsdwe", "master", "~/Desktop/test1") is False


def test_clone_repo_correct_branch():
    """ Contract: Test cloning a known repo with two branches: master and not_master
    The branch not_master should be the one that is cloned
    even though master is the main branch"""
    assert clone_repo("git@github.com:Plongy/test-repo.git", "not_master", "test-repo")

    os.chdir("test-repo")

    output = subprocess.check_output("git branch | grep \*", shell=True)

    os.chdir("..")
    shutil.rmtree("test-repo")

    assert "not_master" in output.decode()


def test_is_successful_command_positive():
    """ Contract : A successful command returns a string which contains "TEST PASSED",
        as such the method should return True """
    output = "Lorem Ipsum dolori yada TEST PASSED nadie pongo"
    success_regex = "TEST PASSED"
    assert (is_successful_command(output, success_regex)) is True


def test_is_successful_command_negative():
    """ Contract: A unsuccessful command returns a string which does not contain "TEST PASSED"
        and therefore the method should return False """
    output = "Lorem Ipsum dolori yada nadie pongo"
    success_regex = "TEST PASSED"
    assert (is_successful_command(output, success_regex)) is False


def test_is_successful_command_regex_positive():
    """ Contract: A successful command returns a string which contains "TEST PASSED",
        as such the method should return True
    """
    output = "Lorem Ipsum dolori yada nadie pongo"
    success_regex = "Ipsum.+yada"
    assert (is_successful_command(output, success_regex)) is True


def test_is_successful_command_regex_negative():
    """ Contract: A bad command returns a string which contains Lorem, but not something else ending in orem,
        as such the method should return False"""
    output = "Lorem Ipsum dolori yada TEST PASSED nadie pongo"
    success_regex = "[^L]orem"
    assert is_successful_command(output, success_regex) is False


def test_is_successful_command_newline_regex_positive():
    """contract : The method should treat new line characters as all other characters"""
    output = "Lorem\n Ipsum dol\nori yada TEST PASSED \nnadie pongo"
    success_regex = "Ipsum.*yada"
    assert is_successful_command(output, success_regex) is True


def test_read_config():
    """Contract: The method correctly reads the config file"""
    m = mock_open(read_data=
                  """{
                    "commands": ["pip install -r requirements.txt", "python runTests.py"],
                    "success_strings": ["", "TESTS PASSED"]
                  }""")

    with patch('CI.CI_helpers.open', m):
        config_data = read_configfile("foo")

    m.assert_called_once_with("foo")

    assert config_data["commands"][0] == "pip install -r requirements.txt"
    assert config_data["success_strings"][0] == ""
    assert config_data["commands"][1] == "python runTests.py"
    assert config_data["success_strings"][1] == "TESTS PASSED"


def test_set_commit_state_1():
    """ Contract: The function posts to the correct url with the correct data. """
    repo = "test/repo"
    sha = "123fgh"
    url = f'https://api.github.com/repos/{repo}/statuses/{sha}?access_token={constants.OAUTH_TOKEN}'
    status = "success"

    with requests_mock.mock() as m:
        m.post(url)
        set_commit_state(repo, sha, status)

    assert m.call_count == 1

    history = m.request_history
    assert history[0].url == url
    assert history[0].method == 'POST'
    assert f'{{"state": "{status}", "context": "continuous-integration/group7-CI"}}' == history[0].text


def test_set_commit_state_2():
    """ Contract: The function posts to the correct url with the correct data (with status parameter set to failure)."""
    repo = "foo/bar"
    sha = "456jgoafj"
    url = f'https://api.github.com/repos/{repo}/statuses/{sha}?access_token={constants.OAUTH_TOKEN}'
    status = "failure"

    with requests_mock.mock() as m:
        m.post(url)
        set_commit_state(repo, sha, status)

    assert m.call_count == 1

    history = m.request_history
    assert history[0].url == url
    assert history[0].method == 'POST'
    assert f'{{"state": "{status}", "context": "continuous-integration/group7-CI"}}' == history[0].text
