import flask
from flask import Blueprint
from myapplication.model import widget
from myapplication.model.db import db_session

app = Blueprint("widgets", __name__)

@app.route("/", methods=("GET", "POST"))
def list_widgets():
    if flask.request.method == "GET":
        return flask.jsonify(widgets=[w.to_json() for w in widget.Widget.query.all()])
    else:
        new_widget = widget.Widget.from_json(flask.request.json)
        db_session.add(new_widget)
        db_session.commit()
        response = flask.jsonify(new_widget.to_json()), 201
        return response

@app.route("/<int:_id>", methods=("PUT", "DELETE", "GET"))
def put_or_delete_widget(_id):
    w = widget.Widget.query.get(_id)
    if flask.request.method == "PUT":
        if w:
            w.update_from_json(flask.request.json)
            db_session.commit()
            return flask.make_response("Success", 200)
        else:
            new_widget = widget.Widget.from_json(flask.request.json)
            new_widget.id = _id
            db_session.add(new_widget)
            db_session.commit()
            response = flask.make_response("Success", 201)
            return response
    elif flask.request.method == "DELETE":
        if w:
            db_session.delete(w)
            db_session.commit()
            return flask.make_response("Deleted", 204)
        else:
            return flask.make_response("Missing", 404)
    else:
        return flask.jsonify(widget=widget.Widget.query.get(_id).to_json())
