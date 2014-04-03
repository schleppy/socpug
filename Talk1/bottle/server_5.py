import bottle
import time

@bottle.route("/beer")
def hello():
    bottle.response.headers['Content-Type'] = 'text/plain'
    for i in range(100, 0, -1):
        if i < 100:
            yield "Take one down, pass it around, " \
                   "{} bottles of beer on the wall\n".format(i)
            time.sleep(.2)
        yield "{} bottles of beer on the wall, " \
               "{} bottles of beer\n".format(i, i)


if __name__ == "__main__":
    bottle.run(debug=True)
