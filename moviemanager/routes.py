from flask import render_template
from moviemanager import app, db, client


@app.route("/")
def home():
    # print(client.search('True Grit'))
    return render_template("base.html")