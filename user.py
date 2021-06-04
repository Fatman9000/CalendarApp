import datetime
import uuid

from flask import session

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.local


class User(object):
    def __init__(self, user_name):
        self.username = user_name

    @classmethod
    def get_by_name(cls, user_name):
        data = db.calendarData.find_one({"username": user_name})
        if data is not None:
            return (data["username"])

    @staticmethod
    def create_user(user_name):
        db.calendarData.insert_one({"username": user_name})

    @staticmethod
    def login_valid(user_name):
        user = User.get_by_name(user_name)
        print(user)
        if user is None:
            User.create_user(user_name)
            user = User.get_by_name(user_name)
        return user == user_name

    @staticmethod
    def login(user_name):
        session["user_name"] = user_name

    @staticmethod
    def get_user_date(date):
        user_date = db.calendarData.find_one({"date": date})
        # datetime.date.strftime()
        if user_date is not None:
            return (user_date["date"])

    @staticmethod
    def store_user_date(date, name):
        check = db.calendarData.find_one({"$and": [{"username" : name}, {date : []}]})
        if check is not None:
            db.calendarData.update_one({"username" : name},{"$set": {date : []}})
    
    @staticmethod
    def store_user_time(name, time, data="Empty"):
        user_date = session["user_date"]
        db.calendarData.update_one({"username" : name} ,{"$push":  {user_date : {time : data}}})
