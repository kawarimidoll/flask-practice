from flask import render_template, redirect, request, url_for, flash
from testapp import app

from testapp import db
from testapp.models.employee import Employee


@app.route("/employees")
def employee_index():
    employees = Employee.query.all()
    return render_template("employees/index.html", employees=employees)


@app.route("/employees/<int:id>")
def employee_show(id):
    employee = Employee.query.get_or_404(id)
    return render_template("employees/show.html", employee=employee)


@app.route("/employees/<int:id>/edit", methods=["GET"])
def employee_edit(id):
    employee = Employee.query.get_or_404(id)
    return render_template("employees/edit.html", employee=employee)


@app.route("/employees/<int:id>/update", methods=["POST"])
def employee_update(id):
    employee = Employee.query.get_or_404(id)
    form_dict = request.form
    employee.name = form_dict.get("name")
    employee.mail = form_dict.get("mail")
    employee.is_remote = form_dict.get("is_remote", default=False, type=bool)
    employee.department = form_dict.get("department")
    employee.year = form_dict.get("year", default=0, type=int)

    db.session.merge(employee)
    db.session.commit()
    flash("employee is updated")
    return redirect(url_for("employee_index"))


@app.route("/employees/<int:id>/delete", methods=["POST"])
def employee_delete(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash("employee is deleted")
    return redirect(url_for("employee_index"))


@app.route("/employees/new")
def employee_new():
    return render_template("employees/create.html")


@app.route("/employees", methods=["POST"])
def employee_create():
    form_dict = request.form

    employee = Employee(
        name=form_dict.get("name"),
        mail=form_dict.get("mail"),
        is_remote=form_dict.get("is_remote", default=False, type=bool),
        department=form_dict.get("department"),
        year=form_dict.get("year", default=0, type=int),
    )

    db.session.add(employee)
    db.session.commit()

    flash("employee is added")
    return redirect(url_for("employee_index"))
