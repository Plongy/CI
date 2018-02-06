from flask import Flask

app = Flask(__name__)

from CI import routes  # NOQA - ignore this in flake8
