from flask import render_template
from testapp import app
from datetime import datetime

today = datetime.today()


@app.route("/")
def index():
    return render_template("testapp/index.html", date_string=today.strftime("%Y-%m-%d"))


@app.route("/about")
def about():
    return "This is about page"
