from flask import render_template, redirect, request, url_for, flash
from testapp import app
from datetime import datetime

from testapp import db
from testapp.models.employee import Employee

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


@app.get("/sampleform")
@app.post("/sampleform")
def sample_form():
    if request.method == "GET":
        print("sampleform GET")
        return render_template("testapp/sampleform.html")
    else:
        # POST request
        print("sampleform POST")
        print(request.form.to_dict())
        return f"POST request received! {request.form['data1']}"


@app.route("/employees")
def employee_list():
    employees = Employee.query.all()
    return render_template("testapp/employees.html", employees=employees)


@app.route("/employees/<int:id>")
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    return render_template("testapp/employee_detail.html", employee=employee)


@app.route("/add_employee", methods=["GET", "POST"])
def add_amployee():
    if request.method == "GET":
        return render_template("testapp/add_employee.html")
    else:
        # POST request
        form_dict = request.form
        print(form_dict)

        employee = Employee(
            name=form_dict.get("name"),
            mail=form_dict.get("mail"),
            is_remote=form_dict.get("is_remote", default=False, type=bool),
            department=form_dict.get("department"),
            year=form_dict.get("year", default=0, type=int),
        )

        db.session.add(employee)
        db.session.commit()

        flash("add employee")
        return redirect(url_for("index"))
