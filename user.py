
import datetime
import json
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
        user_date = db.calendarData.find_one({"$and": [{"username": session["user_name"]}, {session["user_date"] : {"$exists" : "true"}}]})
        if user_date is not None:
            return(user_date[session["user_date"]])

    @staticmethod
    def search_user_entries(search_term):
        print(search_term)
        user_entries = db.calendarData.find({"event_desc": search_term})
        if user_entries is not None:
            return(user_entries)

    @staticmethod
    def store_user_date(date, name):
        check = db.calendarData.find_one({"$and": [{"username": name}, {"user_date" : {date : []}}]})
        if check is not None:
            db.calendarData.update_one({"username": name}, {"$set": {"user_date": {date: []}}})
        
        # print(db.calendarData.index_information())
        # db.calendarData.create_index([('event_desc', 'text')])

    @staticmethod
    def store_user_time(name, time, data="Empty"):
        user_date = session["user_date"]
        # fix this
        db.calendarData.update_one({"username": name}, {"$push": {f"user_date.{user_date}": 
                               {"event_time": time, "event_desc": data}}})
        # db.calendarData.update_one}})

    @staticmethod
    def delete_user_time(name, date, times):
        for item in times:
            item = item.replace("\'",'"')
            json_obj = json.loads(item)
            for key, value in json_obj.items():
                db.calendarData.update_one({"username": name}, {"$pull": {date : {key: value}}})
