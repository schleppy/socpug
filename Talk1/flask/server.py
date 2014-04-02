import flask
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

import myapplication
from myapplication import APP
from myapplication.model.db import db_session
from sqlalchemy import exc


@APP.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

def make_json_app(APP):
    def make_json_error(ex):
        if isinstance(ex, exc.SQLAlchemyError):
            message = str(ex.__class__)
        else:
            message = str(ex)
        response = flask.jsonify(message=message)
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    for code in default_exceptions.iterkeys():
        APP.error_handler_spec[None][code] = make_json_error

    return APP

myapplication.load_blueprints()

APP = make_json_app(APP)

if __name__ == "__main__":
    APP.run('', 8090)
