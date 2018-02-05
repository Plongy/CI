import json

import os

from CI import constants


def log_process(command_list, command_status, command_output, webhook_json):
    """ Takes given webhook data and loads the json to be able to parse it"""
    webhook_data = json.loads(webhook_json)
    data = {
        'date': webhook_data['head_commit']['timestamp'],
        'hash': webhook_data['head_commit']['id'],
        'branch': webhook_data['ref'].split('/')[-1],
        'webhook_data': webhook_data,
        'results': []
    }

    # save date and hash to variables

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
