import uuid
from bson.objectid import ObjectId
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
        if data:
            return (data)

    @staticmethod
    def create_user(user_name):
        user_id = uuid.uuid4()
        db.calendarData.insert_one({"username": user_name, "uuid": user_id})

    @staticmethod
    def login_valid(user_name):
        user = User.get_by_name(user_name)
        if user is None:
            User.create_user(user_name)
            user = User.get_by_name(user_name)
        session["uuid"] = user["uuid"]
        return user["username"] == user_name

    @staticmethod
    def login(user_name):
        session["user_name"] = user_name

    @staticmethod
    def get_by_id(event_id):
        return_date = db.calendarData.find_one({"_id": ObjectId(event_id)})
        if return_date:
            return(return_date)

    @staticmethod
    def get_user_date():
        return_date = db.calendarData.find(
            {"$and": [{"event": {"$exists": True}, "creator_id": session["uuid"]}]})
        if return_date:
            return(return_date)

    @staticmethod
    def search_user_entries(search_term):
        user_entries = db.calendarData.find(
            {"creator_id": session["uuid"], "$text": {"$search": search_term}})
        if user_entries:
            return(user_entries)

    @staticmethod
    def store_user_date(user_datetime, data="Empty"):
        db.calendarData.insert_one(
            {"date_time": user_datetime, "event": data, "creator_id": session["uuid"]})

    @staticmethod
    def update_datetime(event_id, user_datetime, data):
        db.calendarData.update({"_id": ObjectId(event_id)}, {
                               "date_time": user_datetime, "event": data, "creator_id": session["uuid"]})

    @staticmethod
    def delete_user_time(event_id):
        db.calendarData.delete_one({"_id": ObjectId(event_id)})
