from flask import render_template, redirect, request
from testapp import app
from datetime import datetime

today = datetime.today()


@app.route("/")
def index():
    data_dict = {
        "date": today.strftime("%Y-%m-%d"),
        "pages": [
            {"name": "about", "url": "/about"},
            {"name": "page1", "url": "/page/1"},
            {"name": "page2", "url": "/page/2"},
        ],
    }
    return render_template("testapp/index.html", data_dict=data_dict)


@app.route("/about")
def about():
    return render_template("testapp/about.html")


@app.route("/page/")
@app.route("/page/<page_num>")
def page(page_num=None):
    if page_num is None:
        return redirect("/page/1")

    data_dict = {"page_num": int(page_num)}
    return render_template("testapp/page.html", data_dict=data_dict)


@app.get('/sampleform')
@app.post('/sampleform')
def sample_form():
    if request.method == "GET":
        print("sampleform GET")
        return render_template("testapp/sampleform.html")
    else:
        # POST request
        print("sampleform POST")
        print(request.form.to_dict())
        return f'POST request received! {request.form['data1']}'
