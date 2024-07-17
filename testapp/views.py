from flask import render_template
from testapp import app
from datetime import datetime

today = datetime.today()


@app.route("/")
def index():
    data_dict = {
            'date': today.strftime("%Y-%m-%d"),
            'pages': [ 'about', 'page1', 'page2' ]
    }
    return render_template("testapp/index.html", data_dict=data_dict)


@app.route("/about")
def about():
    return "This is about page"

@app.route("/page1")
def page1():
    return "This is page1"

@app.route("/page2")
def page2():
    return "This is page2"
