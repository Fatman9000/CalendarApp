from collections import UserDict
import datetime
import re
import json
from user import User
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
import calendar_app
from pymongo import MongoClient

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"


# @app.before_first_request
# def initialize_userdata():
#     session["userdata"] = calendar_app.pull_user_data()


@app.route("/")
def home_page():
    return render_template("index.html")


@app.route("/validate", methods=["GET", "POST"])
def user_validation():
    user_name = request.form["user_name"]
    User.login(user_name)
    if User.login_valid(user_name):
        return redirect("/calendar")
    else:
        return redirect("/")


@app.route("/calendar", methods=["GET", "POST"])
def date_pick():
    return render_template("calendar.html")


@app.route("/edit", methods=["GET", "POST"])
def date_edit():
    session["user_date"] = request.form["date"]
    User.store_user_date(session["user_date"], session["user_name"])
    events_in_db = User.get_user_date()
    return render_template("edit.html", selected_date=session["user_date"], events=events_in_db)


@app.route("/save", methods=["GET", "POST"])
def save():
    user_time = request.form["time"]
    user_data = request.form["data"]
    to_be_removed = request.form.getlist("remove_event")
    User.delete_user_time(session["user_name"], session["user_date"], to_be_removed)
    if user_time != "" and user_data != "":
        User.store_user_time(session["user_name"], user_time, user_data)
    return redirect("/calendar")
