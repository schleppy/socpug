import bottle

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

if __name__ == "__main__":
    app = bottle.app()
    modified_app = StripPathMiddleware(app)
    bottle.run(app=modified_app)
