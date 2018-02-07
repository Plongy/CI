import os
import shutil

from flask import request

from CI import app
from CI.CI_helpers import \
    set_commit_state, clone_repo, read_configfile, \
    run_commands, is_successful_command
from CI.constants import CLONE_FOLDER, CONF
from CI.history_helpers import log_process


@app.route('/')
def index():
    """The root endpoint, will not be used in the project,
    but is good for checking setups"""
    return 'Hello, World!'


@app.route('/hooks/github', methods=['POST'])
def github_webhook():
    data = request.get_json()
    print(data)

    head_sha = data['head_commit']['id']
    repo_data = data['repository']

    # noinspection PyBroadException
    try:
        set_commit_state(repo_data['full_name'], head_sha, "pending")

        os.makedirs(
            CLONE_FOLDER + repo_data['full_name'],
            exist_ok=True
        )
        clone_repo(
            repo_data['ssh_url'],
            f"{CLONE_FOLDER}{repo_data['full_name']}/{head_sha}"
        )

        config = read_configfile(
            f"{CLONE_FOLDER}{repo_data['full_name']}/{head_sha}/{CONF}"
        )

        # Change to repo folder
        main_dir = os.getcwd()
        os.chdir(f"{CLONE_FOLDER}{repo_data['full_name']}/{head_sha}")

        command_results = run_commands(config['commands'])

        # Return to root folder
        os.chdir(main_dir)
        shutil.rmtree(
            path=f"{CLONE_FOLDER}{repo_data['full_name']}/{head_sha}",
            ignore_errors=True
        )

        successful_commands = [
            is_successful_command(*pair)
            for pair in zip(command_results, config['success_strings'])
        ]

        set_commit_state(
            repo_data['full_name'],
            head_sha,
            "success" if all(successful_commands) else "failure"
        )

        log_process(
            command_list=config['commands'],
            command_status=successful_commands,
            command_output=command_results,
            webhook_json=data
        )
    except Exception as e:
        set_commit_state(
            repo_data['full_name'],
            head_sha,
            "failure"
        )
        print(e)
    return ""  # We have to return something
