import json
import re
import subprocess

import requests

from CI import constants


def clone_repo(ssh_url, branch, target_folder):
    """Pulls the repo at ssh_url into target_folder"""
    command = f'git clone -b {branch} {ssh_url} {target_folder}'
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
        return True
    except subprocess.CalledProcessError as err:
        print(err.returncode)
        return False


def read_configfile(path):
    """Parses a JSON configfile at path and then returns it"""
    json_data = open(path)
    return json.load(json_data)


def run_commands(command_list):
    """Runs a list of bash commands in the current directory
    :type command_list: An iterable containing strings
    Observe: `cd` can not be called with this function
    """
    command_output = []
    for command in command_list:
        split_command = command.split(" ")
        try:
            result = subprocess.Popen(split_command, stdout=subprocess.PIPE)
            # if function call was valid
            if result.returncode is None:
                # append output to list
                command_output.append(result.communicate()[0].decode())
        except OSError as err:
            command_output.append("Error")
            print(err)
    return command_output


def is_successful_command(command_output, success_regex):
    """Returns True iff the command_output matches the success_regex"""
    matcher = re.compile(success_regex, re.DOTALL)
    return bool(matcher.search(command_output))


def set_commit_state(repo_name, commit_hash, state):
    """Sends a POST request to GitHub API according to
    https://developer.github.com/v3/repos/statuses"""
    requests.post(
        url=f"https://api.github.com/repos/{repo_name}/statuses/"
            f"{commit_hash}?access_token={constants.OAUTH_TOKEN}",
        json={
            "state": state,
            "context": "continuous-integration/group7-CI"
        }
    )
