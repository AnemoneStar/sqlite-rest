import flask
from flask import jsonify, make_response, request, current_app
import sqlite3
from functools import update_wrapper

def crossdomain():
    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            h = resp.headers
            h['Access-Control-Allow-Origin'] = "*"
            h['Access-Control-Allow-Methods'] = "GET, HEAD, OPTIONS"
            return resp
        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sqlite3.connect("./test.sqlite")
db.row_factory = dict_factory

app = flask.Flask("sqlite_rest")

@app.route('/')
@crossdomain()
def index():
    return jsonify(db.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall())
@app.route('/<table_name>')
@crossdomain()
def records(table_name):
    if db.execute("SELECT null FROM sqlite_master WHERE type = 'table' AND name = ?", (table_name, )).fetchone() != None:
        return jsonify(db.execute("SELECT * FROM "+table_name).fetchall())
    return jsonify([])
@app.route('/<table_name>/<record_id>')
@crossdomain()
def record_one(table_name, record_id):
    if db.execute("SELECT null FROM sqlite_master WHERE type = 'table' AND name = ?", (table_name, )).fetchone() != None:
        r = db.execute("SELECT * FROM "+table_name + " WHERE id = ?", (record_id, )).fetchall()
        if len(r) == 0:
            return jsonify({}), 404
        return jsonify(r[0])
    return jsonify({}), 404
app.run(port=3000)