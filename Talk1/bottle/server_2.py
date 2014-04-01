import bottle

@bottle.route("/")
def hello():
    return "Hello World!"

@bottle.route("/hello")
@bottle.route("/hello/")
@bottle.route("/hello/<name>")
def hello_name(name="World"):
    return "Hello {}".format(name)

if __name__ == "__main__":
    bottle.run()
