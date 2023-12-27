import os

from flask import Flask
from .logger import Logger


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DB_USER='user',
        DB_PASSWORD='password',
        LOGGER = Logger(__name__+'.log', is_debug_enabled=True)
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #from . import db
    #db.init_app(app)

    from . import temperature_update
    app.register_blueprint(temperature_update.bp)

    #from . import get_data
    #app.register_blueprint(get_data.bp)

    return app