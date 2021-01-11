# -*- config:utf-8 -*-

import sqlite3

import click
from flask import current_app

curr_app = None

def get_db():
    global curr_app
    db = sqlite3.connect(
        curr_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    return db

def init_db():
    global curr_app
    db = get_db()
    try:
        with curr_app.open_resource("schema.sql") as f:
            db.executescript(f.read().decode("utf8"))
        db.commit()
    except sqlite3.Error:
        db.rollback()
    finally:
        db.close()


def init_app(app):
    global curr_app
    curr_app = app
    init_db()
