import os
from flask import Flask, session, render_template, flash, redirect, logging, request, url_for
from flask_session import Session
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from passlib.hash import sha256_crypt
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


@app.route("/")
def homeRoute():
    title = "Home page"
    return render_template("home.html", headerTitle=title)


@app.route("/login")
def loginRoute():
    title = "Login page"
    return render_template("login.html", headerTitle=title)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    username = StringField('Username', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route("/registration", methods=["GET", "POST"])
def registrationRoute():
    title = "Registration page"
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        db.execute(
            "INSERT INTO users (name, email, username, password) VALUES (:n, :e, :u, :p)",
            {"n": name, "e": email, "u": username, "p": password})

        print("New user created")
        db.commit()

        flash('You are now registered and can now log in', 'success')

        return redirect(url_for('homeRoute'))

    return render_template("registration.html", headerTitle=title, form=form)


@app.route("/results")
def resultsRoute():
    title = "Results page"
    return render_template("results.html", headerTitle=title)


@app.route("/book")
def bookRoute():
    title = "Book page"
    return render_template("book.html", headerTitle=title)
