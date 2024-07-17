import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("testapp.config")
app.secret_key = os.environ.get("SECRET_KEY", "default_secret_key")
db = SQLAlchemy(app)

from .models import employee
import testapp.views
