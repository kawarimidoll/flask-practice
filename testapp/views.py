from testapp import app


@app.route("/")
def index():
    return """
<h1>Flask Practice</h1>
<div><em>Hellow World!</em></div>
<div><a href="about">about</a></div>
"""


@app.route("/about")
def about():
    return "This is about page"
