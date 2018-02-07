# CI

A simple CI server created in the course DD2480 at KTH

[Documentation](http://soffun.alexv.se/static/CI.html)


## Running
First you have to install all dependencies with `pip install -r requirements.txt`

The project has been developed in Python 3.6.4

### Environment variables
|Variable       | Default  | Description                                             |
|---------------|----------|---------------------------------------------------------|
|CLONE_FOLDER   |  tmp/    | Folder where to store repos while testing them.         |
|HISTORY_FOLDER | history/ | Folder where to store the history. Should be persistent.|

### Server
The server is run by setting the environment variable `FLASK_APP`
to `CI.py` and starting the server with `flask run`. You can also
run the server by running `python CI.py`

### Tests
The tests are written in pytest and are run by running `pytest` or `py.test`

### Build history for this repository
http://soffun.alexv.se/history/Plongy/CI

### Statement of Contribution
#### Alexander Manske
* Fix: Resolve type mismatch in log_process, update test (see issue #36)
* Feature: Improve logging by printing status messages upon completed tasks during build (see issue #31)
* Feature: Create method that saves output in history file (see issue #9)
* Feature: Create method that runs a list of commands (see issue #7)
* Feature: Create a method for pulling a repository (see issue #5)

#### Alexander Viklund
* Feature: Create code skeleton (see issue #2)
* Feature: Create a weebhook endpoint that runs the whole process (see issue #3)
* Feature: Add support for continuous deployment (see issue #25)
* Fix: Tests are being run on the wrong branch (see issue #30)
* Fix: is_successful_command does not work with responses with newline characters (see issue #32)

#### Alfrida
* Refactor: Method read_configfile should return a json instead of a list (see issue #24)
* Feature: Create a html page and method for showing detailed build info for a specific build (see issue #22)
* Fix: Method run_commands should return strings and not bytestrings (see issue #18)
* Feature: Create method that saves output in history file (see issue #9)
* Feature: Create method that runs a list of commands (see issue #7)
* Feature: Create a method for pulling a repository (see issue #5)

#### Hanna
* Feature: Create method for summarizing the contents of all repo-builds from history. (see issue #29)
* Feature: Create method that builds HTTP-posts with results (see issue #10)
* Feature: Create method that reads config files (see issue #6)
* Feature: Create a page for listing all the builds of a project repo (see issue #21)

#### Lukas
* Feature: Add Travis CI (see issue #1)
* Feature: Create method to determine status of test output (see issue #8)
* Feature: Create method that builds HTTP post with results (see issue #10)
* Feature: Helper method for summarizing the contents of all repo-builds from history (see issue #29)
* Documentation: Fix uniform documentation (see issue #41)
