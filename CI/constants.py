import os

# ignore some line length errors
CLONE_FOLDER = os.getenv('CLONE_FOLDER', 'tmp/')  # NOQA
HISTORY_FOLDER = os.getenv('HISTORY_FOLDER', 'history/')  # NOQA
OAUTH_TOKEN = os.getenv('OAUTH_TOKEN', '1234567890123456789012345678901234567890')  # NOQA

CONF = 'ci_conf.json'
