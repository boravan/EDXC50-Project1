import os
import requests

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["POST", "GET"])
def homeRoute():
    user = request.form.get("email")
    title = "Home page"
    return render_template("home.html", headerTitle=title, userName=user)


@app.route("/login")
def loginRoute():
    title = "Login page"
    return render_template("login.html", headerTitle=title)


@app.route("/registration")
def registrationRoute():
    title = "Registration page"
    return render_template("registration.html", headerTitle=title)


@app.route("/results")
def resultsRoute():
    title = "Results page"
    return render_template("results.html", headerTitle=title)


@app.route("/book")
def bookRoute():
    title = "Book page"
    return render_template("book.html", headerTitle=title)
