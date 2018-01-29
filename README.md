# CI

A simple CI server created in the course DD2480 at KTH


## Running
First you have to install all dependencies with `pip install -r requirements.txt`

The project has been developed in Python 3.6.4

### Server
The server is run by setting the environment variable `FLASK_APP` 
to `CI.py` and starting the server with `flask run`. You can also 
run the server by running `python CI.py`

### Tests
The tests are written in pytest and are run by running `pytest` or `py.test`