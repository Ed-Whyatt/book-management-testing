import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from omdb import OMDBClient
if os.path.exists("env.py"):
    import env  # noqa


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")
app.config["API_KEY"] = os.environ.get("API_KEY")

api_key = os.environ.get("API_KEY")

client = OMDBClient(apikey=api_key)

db = SQLAlchemy(app)

from moviemanager import routes  # noqa
