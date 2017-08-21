import flask
from flask import jsonify
import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sqlite3.connect("./test.sqlite")
db.row_factory = dict_factory

app = flask.Flask("sqlite_rest")

@app.route('/')
def index():
    return jsonify(db.execute("SELECT name FROM sqlite_master WHERE type = 'table'").fetchall())
@app.route('/<table_name>')
def records(table_name):
    return jsonify(db.execute("SELECT * FROM "+table_name).fetchall())
@app.route('/<table_name>/<record_id>')
def record_one(table_name, record_id):
    return jsonify(db.execute("SELECT * FROM "+table_name+" WHERE id = ?", (record_id,)).fetchone())

app.run(port=3000)