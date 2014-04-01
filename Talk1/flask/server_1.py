import flask

app = flask.Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

@app.route("/hello/<name>")
def hello(name="World"):
    return "Hello {}".format(name.title())

@app.route("/fail/<name>")
def fail(name):
    name_to_age = {"sean": 35, "greg": 31, "santa": "100+"}
    return "{} is {} years old".format(name.title(), name_to_age[name])

if __name__ == "__main__":
    app.run(debug=True)
