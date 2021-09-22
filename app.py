from collections import UserDict
import datetime
import re
import json
from user import User
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from pymongo import MongoClient

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"


# @app.before_first_request
# def initialize_userdata():
#     session["userdata"] = calendar_app.pull_user_data()


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


# @app.route("/calendar", methods=["GET"])
# def date_pick():
#     return render_template("calendar.html")


@app.route("/calendar", methods=["GET", "POST"])
def date_edit():
    # session["user_date"] = request.form["user_datetime"]
    # my_var = request.form["user_datetime"] if request.form["user_datetime"] else None
    events_in_db = User.get_user_date()
    events_in_db = [x for x in events_in_db]
    return render_template("edit.html", events=events_in_db)

      
        


@app.route("/save", methods=["GET", "POST"])
def save():
    user_data = request.form["data"]
    selected_date = request.form["user_datetime"]
    try:
        to_be_removed = request.form["remove_event"]
        User.delete_user_time(to_be_removed)
    except:
        pass
    if user_data:
        User.store_user_date(selected_date, user_data)
    events_in_db = User.get_user_date()

    return render_template("edit.html", selected_date=selected_date, events=events_in_db)

@app.route("/search", methods=["GET", "POST"])
def search():
    search_term = request.form["search_term"]
    result = User.search_user_entries(search_term)
    result = [x for x in result]
    print(result)

    return render_template("search.html", search_results=result)