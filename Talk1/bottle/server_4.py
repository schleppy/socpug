import bottle
from werkzeug.debug import DebuggedApplication

class StripPathMiddleware(object):
  def __init__(self, app):
    self.app = app
  def __call__(self, e, h):
    e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
    return self.app(e,h)

@bottle.route("/")
def hello():
    return "Hello World!"

@bottle.route("/hello")
@bottle.route("/hello/<name>")
def hello_name(name="World"):
    return "Hello {}".format(name)

@bottle.route("/fail")
def fail():
    user = bottle.request.params.get("name")
    some_data = {"sean": "admin", "joe": "user"}
    #return "{} is of role {}".format(user, some_data[user])
    return "{} is of role {}".format(user, some_data.get(user, "no role"))

if __name__ == "__main__":
    app = bottle.app()
    app.catchall = False
    debugger_app = DebuggedApplication(app=app, evalex=True)
    modified_app = StripPathMiddleware(debugger_app)
    bottle.run(app=modified_app, debug=True)
