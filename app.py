from collections import UserDict
import datetime
import re
import json
from user import User
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from pymongo import MongoClient, results

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/validate", methods=["POST"])
def user_validation():
    user_name = request.form["user_name"]
    User.login(user_name)
    if User.login_valid(user_name):
        return redirect("/calendar")
    else:
        return redirect("/")


@app.route("/calendar", methods=["GET"])
def date_edit():
    # session["user_date"] = request.form["user_datetime"]
    # my_var = request.form["user_datetime"] if request.form["user_datetime"] else None
    events_in_db = User.get_user_date()
    events_in_db = [x for x in events_in_db]
    if events_in_db == []:
        return render_template("edit.html", events=None)
    else:
        return render_template("edit.html", events=events_in_db)


@app.route("/save", methods=["POST"])
def save():
    user_data = request.form.get("data")
    selected_date = request.form.get("user_datetime")
    if user_data:
        User.store_user_date(selected_date, user_data)
    events_in_db = User.get_user_date()
    return redirect("/calendar")


@app.route("/delete", methods=["POST"])
def delete_event():
    to_be_removed = request.form.get("remove_event")
    if to_be_removed:
        User.delete_user_time(to_be_removed)
    return redirect("/calendar")


@app.route("/update/<event_id>", methods=["GET", "POST"])
def update_event(event_id):
    if request.method == "GET":
        result = User.get_by_id(event_id)
        return render_template("update.html", result=result)
    if request.method == "POST":
        event_datetime = request.form.get("event_datetime")
        event_description = request.form.get("event_description")
        User.update_datetime(event_id, event_datetime, event_description)
        return redirect("/calendar")
        

@app.route("/search", methods=["GET", "POST"])
def search():
    search_term = request.form.get("search_term")
    if search_term:
        result = User.search_user_entries(search_term)
        result = [x for x in result]
        print(result)
        return render_template("search.html", events=result)
    