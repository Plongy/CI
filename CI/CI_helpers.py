import json
import re
import subprocess


def clone_repo(ssh_url, target_folder):
    """Pulls the repo at ssh_url into target_folder"""
    command = 'git clone ' + ssh_url + ' ' + target_folder
    try:
        process = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
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
            if result.returncode == None:
                # append output to list
                command_output.append(result.communicate()[0].decode())
        except OSError as err:
            command_output.append("Error")
            print(err)
    return command_output


def is_successful_command(command_output, success_regex):
    """Returns True iff the command_output matches the success_regex"""
    matcher = re.compile("^.*" + success_regex + ".*$")
    return bool(matcher.match(command_output))


def set_commit_state(repo_url, commit_hash, state):
    """Sends a POST request to GitHub API according to
    https://developer.github.com/v3/repos/statuses"""
    raise NotImplementedError
