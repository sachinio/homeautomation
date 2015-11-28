# ------ DATABASE --------
import sqlite3
from flask import g

DATABASE = 'homeAutomation.db'


def init_db(app):
    with app.app_context():
        db = get_db()
        with app.open_resource('homeAutomation.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect(DATABASE)


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db


def update(table, field, value):
    db = get_db()
    db.execute("UPDATE %s SET value='%s' WHERE name='%s'" % (table, value, field))
    db.commit()


def insert(table, fields=(), values=()):
    db = get_db()
    cur = db.cursor()
    query = 'INSERT INTO %s (%s) VALUES (%s)' % (
        table,
        ', '.join(fields),
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    db.commit()
    id = cur.lastrowid
    cur.close()
    return id


def test():
    for setting in query_db('select * from settings'):
        print setting[1], 'has value of', setting[2]


