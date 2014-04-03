import flask
from flask.ext import login
from form import form_login
from model import user

app = flask.Flask(__name__)
app.config.from_object("config")
login_manager = login.LoginManager()
login_manager.init_app(app)

User = {"sean": "beans", "joe": "potatoes"}

@app.before_request
def set_user():
    flask.g.user = login.current_user

@login_manager.user_loader
def load_user(userid):
    return user.User(userid)

@app.route("/")
def home():
    return flask.render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login_page():
    form = form_login.LoginForm()
    if form.validate_on_submit():
        the_user = user.User(form.username.data)
        login.login_user(the_user)
        flask.flash("Logged in successfully.")
        return flask.redirect(flask.request.args.get("next") or flask.url_for("home"))
    else:
        print form.errors
    return flask.render_template("login.html", form=form)

@app.route("/secret")
@login.login_required
def sercret():
    return flask.render_template("secret.html")

@app.route("/logout")
@login.login_required
def logout():
    login.logout_user()
    flask.flash("You have been logged out.")
    return flask.redirect(flask.url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
