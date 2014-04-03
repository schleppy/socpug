import os
import importlib
import flask
from werkzeug.routing import BaseConverter
from sqlalchemy import exc
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

class RegexConverter(BaseConverter):
    """
    Regular expression converter for routes
    """
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

# Set up the application
APP = flask.Flask(__name__)
APP.config.from_object("myapplication.config")
APP.url_map.converters['re'] = RegexConverter

def load_blueprints():
    blueprints_directory = APP.config.get("BLUEPRINTS_DIRECTORY")
    if not blueprints_directory:
        raise Exception("You must define BLUEPRINTS_DIRECTORY in your config")
    endpoints_directory = os.path.join(os.path.dirname(__file__), blueprints_directory)
    endpoint_module_path = "{}.{}".format(APP.config.get("APP_NAME"), blueprints_directory.replace("/", "."))
    endpoints = ["{}.{}".format(endpoint_module_path, os.path.splitext(f)[0]) for f in 
        os.listdir(endpoints_directory) if f.endswith(".py") and not f.startswith("__")]

    for endpoint in endpoints:
        try:
            module = importlib.import_module(endpoint)
        except ImportError as ie:
            continue
        if hasattr(module, 'app'):
            print "Adding blueprint for {}".format(endpoint)
            APP.register_blueprint(module.app, url_prefix="/{}".format(endpoint.split(".")[-1]))


def make_json_app(APP):
    def make_json_error(ex):
        if isinstance(ex, exc.SQLAlchemyError):
            message = str(ex.__class__)
        else:
            message = str(ex)
        print str(ex)
        response = flask.jsonify(message=message)
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    for code in default_exceptions.iterkeys():
        APP.error_handler_spec[None][code] = make_json_error

    return APP
