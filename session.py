# -*- coding: utf-8 -*-
from flask import Flask, request
from db import DBWorker, check_arguments
from sqlite3 import Error
from uuid import uuid4
import json
from connection import ConnectionInfo, Connections

app = Flask(__name__)


@app.route("/login")
def login():
    try:
        if not check_arguments(['login', 'password'], request.args):
            raise Error('Bad arguments')

        login = request.args.get('login')
        password = request.args.get('password')

        if db_worker.confirm_login_data(login, password):
            code = "".join(str(uuid4()).split('-'))
            if connections.find(ConnectionInfo(login, code)):
                raise Error("You logged already")

            item = ConnectionInfo(login, code)
            connections.add(item)
            return json.dumps({'code': code})

        raise Error("No such login and password")

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/logout")
def logout():
    try:
        if not check_arguments(['login', 'code'], request.args):
            raise Error("Bad arguments")

        login = request.args.get("login")
        code = request.args.get("code")
        if connections.remove(login, code):
            return json.dumps({'ok': 'ok'})

        raise Error("You not logged yet")

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/check_connection")
def check_connection():
    try:
        if not check_arguments(['login', 'code'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get("login")
        code = request.args.get("code")
        if connections.find(ConnectionInfo(login, code)):
            return json.dumps({'ok': 'ok'})

        raise Exception("Access denied")

    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    db_worker = DBWorker()
    connections = Connections()
    app.run(debug=True, port=65011)

