from sqlalchemy import Column, Integer, String
from myapplication.model.db import Base

class Widget(Base):

    __tablename__ = 'widgets'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    size = Column(String(20))

    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __repr__(self):
        return '<Widget %r: %r>' % (self.name, self.size)

    def update_from_json(self, json):
        for k, v in json.items():
            if self.__dict__.get(k):
                setattr(self, k, v)

    @classmethod
    def from_json(cls, json):
        return cls(json.get('name'), json.get('size'))
