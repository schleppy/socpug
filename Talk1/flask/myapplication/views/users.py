import flask
from flask import Blueprint
from myapplication.model import widget
from myapplication.model.db import db_session
from myapplication import views
from flask.views import MethodView
from myapplication.model import user
from myapplication.model.db import db_session

bp_name = __name__.split(".")[-1]
app = Blueprint(bp_name, __name__)

class UsersAPI(MethodView):

    def get(self, _id=None):
        if _id:
            return flask.jsonify(user.User.query.get(_id).to_json())
        return flask.jsonify(users=[u.to_json() for u in user.User.query.all()])

    def post(self):
        new_user = user.User.from_json(flask.request.json)
        db_session.add(new_user)
        try:
            db_session.commit()
        except:
            raise Exception("Insert failed")
        return flask.jsonify(new_user.to_json()), 201

    def delete(self, _id):
        u = user.User.query.get(_id)
        db_session.delete(u)
        db_session.commit()
        return flask.make_response("Deleted", 204)

    def put(self, _id):
        u = user.User.query.get(_id)
        if u:
            u.update(flask.request.json)
            db_session.commit()
            return flask.jsonify(u.to_json())
        else:
            u = user.User.from_json(flask.request.json)
            u.id = _id
            db_session.add(u)
            db_session.commit()
            return flask.jsonify(u.to_json())

    def patch(self, _id):
        print "RUNNING PATCH..."
        u = user.User.query.get(_id)
        if not u:
            return "Missing", 404
        print flask.request.json
        print u.__dict__
        print _id
        u.update(flask.request.json)
        db_session.commit()
        return flask.jsonify(u.to_json())




views.register_api(app, UsersAPI, bp_name, '/', pk='_id')
