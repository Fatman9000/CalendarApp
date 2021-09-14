
import datetime
import json
from threading import Event
import uuid

from flask import session

from pymongo import MongoClient, TEXT

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
        if user is None:
            User.create_user(user_name)
            user = User.get_by_name(user_name)
        return user == user_name

    @staticmethod
    def login(user_name):
        session["user_name"] = user_name

    @staticmethod
    def get_user_date():
        return_date = db.calendarData.find_one({"username": session["user_name"]})
        print(return_date)
        if return_date is not None:
            return(return_date["user_date"])

    @staticmethod
    def search_user_entries(search_term):
        # db.calendarData.create_index([('event_desc', TEXT)])
        print(search_term)
        user_entries = db.calendarData.find({"$text":{"$search": "meeting"}})
        print(user_entries)
        if user_entries is not None:
            return(user_entries)

    @staticmethod
    def store_user_date(user_datetime, name, data="Empty"):
        # check = db.calendarData.find_one({"$and": [{"username": name}, {"user_date" : {"date" : user_datetime}}]})
        # if check is None:
        db.calendarData.update_one({"username": name}, {"$push": {"user_date": {"date_time" : user_datetime, "event" : data}}})
    @staticmethod
    def store_user_time(name, time, data="Empty"):
        selected_date = session["user_date"]
        db.calendarData.update_one({"$and" : [{"username": name}, {"user_date.date" : selected_date}]}, {"$push": {"user_date": {"date" : selected_date}, "events" : [{data : time}]}})
    
    @staticmethod
    def delete_user_time(name, events):
        selected_date = session["user_date"]
        for item in events:
            print(item)
            item = item.replace("\'",'"')
            json_obj = json.loads(item)
            for key, value in json_obj.items():
                db.calendarData.update_one({"username": name}, {"$pull": {"user_date" : {key: value}}})
            