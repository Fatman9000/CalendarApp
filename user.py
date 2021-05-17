import datetime
import uuid

from flask import session

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db=client.calendarData


class User(object):
    def __init__(self, username):
        self.username = username
        
    @classmethod
    def get_by_name(cls, username):
        data = db.find_one({"username": username})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(username):
        user = User.get_by_name(username)
        if user is not None:
            return user.username == username
        return False

    @staticmethod
    def login(username):
        session["username"] = username