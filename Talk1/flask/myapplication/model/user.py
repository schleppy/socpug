from sqlalchemy import Column, Integer, String
from myapplication.model.db import Base

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.name

    def __repr__(self):
        return '<User %r: %r>' % (self.name, self.email)

    @classmethod
    def from_json(cls, json):
        return cls(json.get('name'), json.get('email'))
