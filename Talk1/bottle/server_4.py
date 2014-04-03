import bottle
from werkzeug.debug import DebuggedApplication
from middleware import StripPathMiddleware


@bottle.route("/fail")
def fail():
    user = bottle.request.params.get("name")
    some_data = {"sean": "admin", "joe": "user"}
    return "{} is of role {}".format(user, some_data[user])

if __name__ == "__main__":
    app = bottle.app()
    app.catchall = False
    debugger_app = DebuggedApplication(app=app, evalex=True)
    modified_app = StripPathMiddleware(debugger_app)
    bottle.run(app=modified_app, debug=True)
