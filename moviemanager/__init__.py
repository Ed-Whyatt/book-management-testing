import os
import re
from flask import Flask
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from omdb import OMDBClient
if os.path.exists("env.py"):
    import env  # noqa


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["API_KEY"] = os.environ.get("API_KEY")


db = SQLAlchemy(app)
mongo = PyMongo(app)
api_key = os.environ.get("API_KEY")
client = OMDBClient(apikey=api_key)

from moviemanager import routes  # noqa