import mongoengine as me
from flask_mongoengine import MongoEngine

from .classifiers import Classifier
__all__ = ["Classifier"]


db = MongoEngine()


def init_db(app):
   db.init_app(app)
