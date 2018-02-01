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
    assert clone_repo("fsdwe", "~/Desktop/test1") == False
