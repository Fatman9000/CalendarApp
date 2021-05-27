import os
import requests
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.calendarData


def pull_user_data():
    existing_userdata = db
    return existing_userdata


def insert_user_data():
    db.insert_one()


