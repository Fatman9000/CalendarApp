from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


# @app.before_first_request()
# def initialize_userdata():
#     session["userdata"]
    

@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/validate',methods=['GET', 'POST'])
def user_validation():
    user = request.form['username']
    session["username"] = user
    return redirect("/")
    
    