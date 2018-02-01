from unittest.mock import mock_open, patch

from CI.CI_helpers import *


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


def test_clone_repo():
    """ Will return false since we are trying to clone a non-existing repo"""
    assert clone_repo("fsdwe", "~/Desktop/test1") is False


def test_is_successful_command_positive():
    # contract : A successful command returns a string which contains "TEST PASSED"
    # as such the method should return True
    output = "Lorem Ipsum dolori yada TEST PASSED nadie pongo"
    success_regex = "TEST PASSED"
    assert (is_successful_command(output, success_regex)) is True


def test_is_successful_command_negative():
    # contract: A unsuccessful command returns a string which does not contain "TEST PASSED"
    # and therefore should return False
    output = "Lorem Ipsum dolori yada nadie pongo"
    success_regex = "TEST PASSED"
    assert (is_successful_command(output, success_regex)) is False


def test_is_successful_command_regex_positive():
    # contract : A successful command returns a string which contains "TEST PASSED"
    # as such the method should return True
    output = "Lorem Ipsum dolori yada nadie pongo"
    success_regex = "Ipsum.+yada"
    assert (is_successful_command(output, success_regex)) is True


def test_is_successful_command_regex_negative():
    # contract : A successful command returns a string which contains "TEST PASSED"
    # as such the method should return True
    output = "Lorem Ipsum dolori yada TEST PASSED nadie pongo"
    success_regex = "[^L]orem"
    assert is_successful_command(output, success_regex) is False


def test_read_config():
    m = mock_open(read_data=
                  """{
                    "commands": ["pip install -r requirements.txt", "python runTests.py"],
                    "success_strings": ["", "TESTS PASSED"]
                  }""")

    with patch('CI.CI_helpers.open', m):
        commands, success = read_configfile("foo")

    m.assert_called_once_with("foo")

    assert commands[0] == "pip install -r requirements.txt"
    assert success[0] == ""
    assert commands[1] == "python runTests.py"
    assert success[1] == "TESTS PASSED"


def test_log_process_positive():
    """ Checks if a log file with the given data is
    written to the given file path"""
    command_list = ["echo hello", "echo bye"]
    command_status = [True, True]
    command_output = [b'hello\n', b'bye\n']
    # file path of the webhook data
    path = os.getcwd() + '/test/webhook_test.json'

    assert log_process(command_list, command_status, command_output, path) is True
