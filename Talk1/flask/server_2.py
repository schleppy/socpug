import flask
import time

app = flask.Flask(__name__)

@app.route("/beer")
def beer():
    def yield_beer():
        for i in range(100, 0, -1):
            if i < 100:
                yield "Take one down, pass it around, {} bottles of beer on the wall\n".format(i)
                time.sleep(0.2)
            yield "{} bottles of beer on the wall, {} bottles of beer\n".format(i, i)
    return flask.Response(yield_beer())

if __name__ == "__main__":
    app.run(debug=True)
