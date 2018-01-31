def pull_repo(ssh_url, target_folder):
    """Pulls the repo at ssh_url into target_folder"""
    raise NotImplementedError


def read_configfile(path):
    """Parses a JSON configfile at path and then returns it"""
    raise NotImplementedError


def run_commands(command_list):
    """Runs a list of bash commands in the current directory
    :type command_list: An iterable containing strings
    """
    raise NotImplementedError


def is_successful_command(command_output, success_regex):
    """Returns True iff the command_output matches the success_regex"""
    raise NotImplementedError


def set_commit_state(repo_url, commit_hash, state):
    """Sends a POST request to GitHub API according to https://developer.github.com/v3/repos/statuses"""
    raise NotImplementedError
