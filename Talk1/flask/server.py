import flask

import myapplication
from myapplication import APP
from myapplication.model.db import db_session


@APP.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


myapplication.load_blueprints()
APP = myapplication.make_json_app(APP)

if __name__ == "__main__":
    APP.run('', 8090)
