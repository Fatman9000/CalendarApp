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
    username = request.form["username"]
    User.login(username)
    print(session["username"])
    # return redirect("/")
    if User.login_valid(username):
        return redirect("/calendar")
    else:
        return redirect("/")


@app.route("/calendar", methods=["GET", "POST"])
def date_pick():
    print(session["username"])
    return render_template("calendar.html")


@app.route("/edit", methods=["GET", "POST"])
def date_edit():
    pass
