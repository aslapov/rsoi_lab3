# -*- coding: utf-8 -*-
from flask import Flask, request
from db import DBWorker, check_arguments
import json
from sqlite3 import Error

app = Flask(__name__)


@app.route("/me")
def me():
    try:
        if not check_arguments(['login'], request.args):
            raise Error("Bad arguments")

        login = request.args.get('login')
        result = db_worker.get_user_data_by_login(login)
        if len(result) != 0:
            return json.dumps(result[0])

        raise Error("No such user")

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/add_login", methods=['POST'])
def add_login():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'password'], data_json):
            raise Error("Bad arguments")

        db_worker.insert_into_login_data_table(data_json['login'], data_json['password'])

        return json.dumps({'ok': 'ok'})

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/add_user", methods=['POST'])
def add_user():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'first', 'second', 'age', 'city',
                                'email', 'like', 'my'], data_json):
            raise Error("Bad arguments")

        db_worker.insert_into_users_data_table(data_json['login'], data_json['first'], data_json['second'],
                                               data_json['age'], data_json['city'], data_json['email'],
                                               data_json['like'], data_json['my'])

        return json.dumps({'ok': 'ok'})

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/remove_login", methods=['DELETE'])
def remove_login():
    try:
        data_json = request.get_json()
        if not check_arguments(['login'], data_json):
            raise Error("Bad arguments")

        db_worker.delete_from_login_data_table(data_json['login'])

        return json.dumps({'ok': 'ok'})

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/remove_user", methods=['DELETE'])
def remove_user():
    try:
        data_json = request.get_json()
        if not check_arguments(['login'], data_json):
            raise Error("Bad arguments")

        db_worker.delete_from_users_data_table(data_json['login'])

        return json.dumps({'ok': 'ok'})

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/update_user", methods=['PUT'])
def update_user():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'first', 'second', 'age', 'city',
                                'email', 'like', 'my'], data_json):
            raise Error("Bad arguments")

        db_worker.update_users_data_table(data_json['login'], data_json['first'], data_json['second'],
                                          data_json['age'], data_json['city'], data_json['email'],
                                          data_json['like'], data_json['my'])

        return json.dumps({'ok': 'ok'})

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/user/<_id>")
def user_info(_id):
    try:
        result = db_worker.get_user_data_by_id(_id)
        if len(result) != 0:
            return json.dumps(result[0])

        raise Error("No user with such id {0}".format(_id))

    except Error as e:
        return json.dumps({'error': str(e)})


@app.route("/login_to_id")
def login_to_id():
    try:
        if not check_arguments(['login'], request.args):
            raise Error("Bad arguments")

        login = request.args.get('login')
        result = db_worker.get_id_by_login(login)
        if len(result) != 0:
            return json.dumps(result[0])

        raise Error("No user with such login {0}".format(login))

    except Error as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    db_worker = DBWorker()
    app.run(debug=True, port=65012)