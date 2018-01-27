from CI import app


@app.route('/')
def index():
    """The root endpoint, will not be used in the project, but is good for checking setups"""
    return 'Hello, World!'
