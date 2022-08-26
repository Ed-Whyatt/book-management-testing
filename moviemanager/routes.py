from flask import flash, render_template, request, redirect, session, url_for
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from moviemanager import app, db, mongo, client
from moviemanager.models import Category, Users


@app.route("/")
@app.route("/get_movies")
def get_movies():
    movies = mongo.db.movies.find()
    return render_template("movies.html", movies=movies)