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
        # Attributes of that exception hold the arguments,
        # the exit code, and stderr.
        print("Exception: CalledProcessError. Return code:", err.returncode)
        return False


def read_configfile(path):
    """Parses a JSON configfile at path and then returns it"""
    json_data = open(path)
    return json.load(json_data)


def run_commands(command_list):
    """Runs a list of bash commands in the current directory
    command_list: An iterable containing strings
    Observe: `cd` can not be called with this function
    """
    command_output = []
    for command in command_list:
        split_command = command.split(" ")
        try:
            result = subprocess.Popen(split_command, stdout=subprocess.PIPE)
            # if function call was valid
            result.wait()
            command_output.append((result.returncode, result.communicate()[0].decode()))
        except OSError as err:
            command_output.append((1, "Error"))
            print("Exception: OSError", err)
    return command_output


def is_successful_command(command_output, success_regex):
    """Returns True iff the command_output matches the success_regex"""
    if command_output[0] != 0:
        return False
    matcher = re.compile(success_regex, re.DOTALL)
    return bool(matcher.search(command_output[1]))


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


def try_deploy(config):
    """Tries to deploy the tested application
    according to the data in config

    The method takes a dictionary that contains
    the following key-value pairs:
    'deploy_ssh_url' - the target ssh_url to deploy to
    'source_branch' - the branch that should be deployed
    'target_branch' - the target branch to deploy to
    """
    if "deploy_ssh_url" not in config:
        return "No deploy config"
    target_url = config['deploy_ssh_url']
    source_branch = config['source_branch']
    target_branch = config['target_branch']

    repo_current_branch = subprocess.check_output(
        "git branch | grep \*",
        shell=True
    )

    branch = repo_current_branch.decode()[2:-1]

    if source_branch == branch:
        return subprocess.getoutput(
            f"git push {target_url} {source_branch}:{target_branch}"
        )
    else:
        return "Did not deploy"
