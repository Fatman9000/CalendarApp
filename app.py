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
    try:
        session["user_date"] = request.form["date"]
    except:
        pass
    User.store_user_date(session["user_date"], session["user_name"])
    events_in_db = User.get_user_date()
    if events_in_db == []:
        return render_template("edit.html", selected_date=session["user_date"], events=None)
    else:
        return render_template("edit.html", selected_date=session["user_date"], events=events_in_db)
        


@app.route("/save", methods=["GET", "POST"])
def save():
    user_time = request.form["time"]
    user_data = request.form["data"]
    to_be_removed = request.form.getlist("remove_event")
    User.delete_user_time(session["user_name"], session["user_date"], to_be_removed)
    if user_time != "" and user_data != "":
        User.store_user_time(session["user_name"], user_time, user_data)
    return redirect("/edit")

@app.route("/search", methods=["GET", "POST"])
def search():
    search_term = request.form["search_term"]
    results = User.search_user_entries(search_term)
    print(results)
    # del results["_id"]
    # del results["username"]
    # matching_results = {}
    # print(results)

    # for k in results:
    #     for v in results[k]:
    #         if search_term in v.values():
    #             print(search_term,v)
    #             matching_results.setdefault(k,v)
    # print(matching_results)

    return render_template("search.html", search_results=results)