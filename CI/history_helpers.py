import json
import os

from CI import constants


def log_process(command_list, command_status, command_output, webhook_data):
    """ Takes given webhook data and loads the json to be able to parse it"""
    # save date, hash and branch to variables
    data = {
        'date': webhook_data['head_commit']['timestamp'],
        'hash': webhook_data['head_commit']['id'],
        'branch': webhook_data['ref'].split('/')[-1],
        'webhook_data': webhook_data,
        'results': []
    }

    # start building our log entry
    for i in range(len(command_list)):
        data['results'].append({
            'command': command_list[i],
            'status': command_status[i],
            'output': command_output[i]
        })

    # 'full_name' is on the form {author}/{repo}
    repo_author_and_name = webhook_data['repository']['full_name']

    # logfile path: history/author/repo/[build_index].json
    log_dir = constants.HISTORY_FOLDER + repo_author_and_name
    number_of_files = 0
    try:
        number_of_files = len(os.listdir(log_dir))
    except FileNotFoundError as error:
        print(error)

    data['id'] = number_of_files
    os.makedirs(log_dir, exist_ok=True)
    log_dir = log_dir + "/" + str(number_of_files) + '.json'

    # save log entry to file
    try:
        with open(log_dir, 'w') as outfile:
            outfile.write(json.dumps(data))

    except IOError as e:
        print("Error writing to file.", e, "Tried to write", data)


def get_builds(owner, repo_name):
    """Takes the owner (/author) and name of repository
     and returns a list containing information from all builds
     for that repository.
     The information contained in each build:
     id, commit message, hash, status, branch, date"""
    path = f"History/{owner}/{repo_name}/"
    build_list = []
    try:
        number_of_files = len(os.listdir(path))
    except FileNotFoundError as error:
        print(error)
    try:
        for i in range(number_of_files):
            index = str(i) + ".json"
            path = path + index
            with open(path) as json_file:
                data = json.load(json_file)
                cmd_res = data["results"]
                build_list.append({
                    'date': data['date'],
                    'id': data['id'],
                    'message': data['head_commit']['message'],
                    'hash': data['hash'],
                    'status': all(
                        [cmd_res[i]["status"] for i in range(len(cmd_res))]
                    ),
                    'branch': data['branch']
                })

    except FileNotFoundError as error:
        print(error)
    return build_list
