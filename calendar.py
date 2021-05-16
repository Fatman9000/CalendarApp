import os, requests
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db=client.calendarData

def pull_user_data():
    existing_userdata = db