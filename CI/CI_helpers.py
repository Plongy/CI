import json
import re
import subprocess
import os


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
    data = json.load(json_data)
    commands = data["commands"]
    success_strings = data["success_strings"]
    return commands, success_strings


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


def log_process(command_list, command_status, command_output, path):
    """ Takes given data and saves it to a log file under /history/log_hash.json"""
    data = {}

    # open json data from webhook
    with open(path) as jdata:
        jsondata = json.load(jdata)
        # save date and hash to variables
        data['date'] = jsondata['head_commit']['timestamp']
        data['hash'] = jsondata['head_commit']['id']

    jdata.close()

    data['results'] = []
    # start building our log entry
    for i in range(len(command_list)):
        command = command_list[i]
        status = command_status[i]
        output = command_output[i].decode('utf-8')
        data['results'].append({
            'command': command,
            'status': status,
            'output': output
        })

    # logfile name convention: log_hash.json
    log_dir = os.getcwd() + '/history/log_' + data['hash'] + '.json'
    # save log entry
    try:
        with open(log_dir, 'w') as outfile:
            json.dump(data, outfile)
        return True

    except IOError:
        return False
