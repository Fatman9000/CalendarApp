import datetime
import re
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
    # print(session["user_name"])
    return render_template("calendar.html")


@app.route("/edit", methods=["GET", "POST"])
def date_edit():
    # user_date = datetime.date.fromisoformat(request.form["date"])
    user_date = request.form["date"]
    # print(session["user_date"])
    User.store_user_date(user_date, session["user_name"])
    # events_in_db = 
    return render_template("edit.html", selected_date=user_date)

@app.route("/save", methods=["GET", "POST"])
def save():
    user_time = request.form["time"]
    user_data = request.form["data"]
    User.store_user_time(session["user_name"],user_time, user_data)
    return redirect("/calendar")