import datetime
import uuid

from flask import session

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.local


class User(object):
    def __init__(self, username):
        self.username = username

    @classmethod
    def get_by_name(cls, username):
        data = db.calendarData.find_one({"username": username})
        if data is not None:
            return (data["username"])

    @staticmethod
    def create_user(username):
        db.calendarData.insert_one({"username": username})

    @staticmethod
    def login_valid(username):
        user = User.get_by_name(username)
        print(user)
        if user is None:
            User.create_user(username)
            user = User.get_by_name(username)
        return user == username

    @staticmethod
    def login(username):
        session["username"] = username
