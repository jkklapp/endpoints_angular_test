"""Contains the definition of the application's basic models.
"""
from google.appengine.ext import ndb

class GreetingModel(ndb.Model):
    """Greeting that stores a message."""
    text = ndb.StringProperty(default="Hi")
    author = ndb.StringProperty(default="Anon", required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def get_by_id(cls, key):
        element = ndb.Key(cls, key)
        return element.get()

    @classmethod
    def all(cls):
        return cls.query().fetch()
