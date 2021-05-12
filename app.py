from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)

from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'


@app.route('/')
def home_page():
    return render_template("index.html")
