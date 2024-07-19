# flask-practice

flask practice https://flask.palletsprojects.com/en/3.0.x/

## develop

### initialize

```sh
python -m venv .venv
```

### run server

```sh
. .venv/bin/activate

python server.py

deactivate
```

### create db

```sh
❯ python
Python 3.12.4 (main, Jul 13 2024, 23:31:13) [Clang 17.0.6 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from testapp import app,db
>>> with app.app_context():
...     db.create_all()
...
>>>
```

### add modules

make sure you are in virtual environment

#### add new modules

```sh
pip install flask
pip freeze > requirements.txt
```

#### add modules from requirements.txt

```sh
pip install -r requirements.txt
```

### test

```sh
pytest
```

with print output:

```sh
pytest -s
```

## reference

https://qiita.com/Bashi50/items/30065e8f54f7e8038323
