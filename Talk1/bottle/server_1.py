import bottle

@bottle.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    bottle.run()
