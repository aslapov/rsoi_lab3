# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, session
import requests
import json
import os

app = Flask(__name__)


def get_layer_url(url_part):
    return "http://localhost:65014/" + url_part


def get_data_from_cookies():
    return session.get('login'), session.get('code')


def set_data_to_cookies(login, code):
    session['login'] = login
    session['code'] = code


def clear_data_in_cookies():
    session.pop('login', None)
    session.pop('code', None)


@app.route("/")
def home():
    if not ('login' in session and 'code' in session):
        return render_template("login_form.html")

    return render_template("main_form.html")


@app.route("/login", methods=['POST'])
def login():
    if 'reg' in request.form:
        return render_template("registration_form.html")

    if not ('login' in session and 'code' in session):
        login = request.form["login"]
        password = request.form["pwd"]

        url = get_layer_url("login") + "?login={0}&password={1}".format(login, password)

        result = requests.get(url).json()

        if 'error' in result:
            return result['error']

        session.permanent = True
        set_data_to_cookies(login, result['code'])

    return render_template("main_form.html")


@app.route("/logout")
def logout():
    login, code = get_data_from_cookies()
    url = get_layer_url("logout") + "?login={0}&code={1}".format(login, code)

    result = requests.get(url).json()

    if 'error' in result:
        return result['error']

    clear_data_in_cookies()

    return render_template("login_form.html")


@app.route("/registration", methods=['POST'])
def registration():
    login = request.form['login']
    first = request.form['first']
    second = request.form['second']
    age = request.form['age']
    city = request.form['city']
    email = request.form['email']
    like = request.form['like']
    my = request.form['my']
    password = request.form['password']

    url = get_layer_url("add_user")
    data = {'login': login, 'first': first, 'second': second, 'age': age,
            'city': city, 'email': email, 'like': like, 'my': my, 'password': password}
    headers = {'Content-type': 'application/json'}

    result = requests.post(url, data=json.dumps(data), headers=headers).json()

    if 'error' in result:
        return result['error']

    return render_template("login_form.html")


@app.route("/me")
def me():
    login, code = get_data_from_cookies()

    url = get_layer_url("me") + "?login={0}&code={1}".format(login, code)

    result = requests.get(url).json()

    if 'error' in result:
        return result['error']

    return render_template("me_form.html", user=result)


@app.route("/remove_user")
def remove_user():
    url = get_layer_url("remove_user")
    login, code = get_data_from_cookies()
    data = {'login': login, 'code': code}
    headers = {'Content-type': 'application/json'}

    result = requests.delete(url, data=json.dumps(data), headers=headers).json()

    if 'error' in result:
        return result['error']

    clear_data_in_cookies()

    return render_template("login_form.html")


@app.route("/edit_user")
def edit_user():
    login, code = get_data_from_cookies()
    url = get_layer_url("get_user_info?login={0}&code={1}".format(login, code))
    result = requests.get(url).json()

    if 'error' in result:
        return result['error']

    return render_template("edit_user_form.html", user=result)


@app.route("/update_user", methods=['POST'])
def update_user():
    first = request.form['first']
    second = request.form['second']
    age = request.form['age']
    city = request.form['city']
    email = request.form['email']
    like = request.form['like']
    my = request.form['my']

    url = get_layer_url("update_user_info")
    login, code = get_data_from_cookies()
    data = {'login': login, 'code': code, 'first': first,
            'second': second, 'age': age, 'city': city, 'email': email, 'like': like, 'my': my}
    headers = {'Content-type': 'application/json'}

    result = requests.put(url, data=json.dumps(data), headers=headers).json()

    if 'error' in result:
        return result['error']

    return render_template("main_form.html")


@app.route("/bikes")
def bikes():
    return render_template("bikes_form.html")


@app.route("/show_bikes", methods=['GET', 'POST'])
def show_bikes():
    login, code = get_data_from_cookies()

    _id = request.args.get('_id')
    url = get_layer_url("get_user_by_id") + "?login={0}&code={1}&_id={2}".format(login, code, _id)
    result = requests.get(url).json()
    if 'error' in result:
        return result['error']
    user = result
    
    if request.args.get('like'):
        url = get_layer_url("like_bikes?login={0}&code={1}&id={2}".
                            format(login, code, _id))
        template = "like_bikes_form.html"
    else:
        url = get_layer_url("my_bikes?login={0}&code={1}&id={2}".
                            format(login, code, _id))
        template = "my_bikes_form.html"

    result = requests.get(url).json()
    if 'error' in result:
        return result['error']

    return render_template(template, bikes=result, user=user)


@app.route("/catalog", methods=['GET', 'POST'])
def catalog():
    global page
    if 'prev' in request.form:
        page -= 1
    elif 'next' in request.form:
        page += 1
    else:
        page = 1

    url = get_layer_url("catalog?page={0}".format(page))

    result = requests.get(url).json()
    if 'error' in result:
        return result['error']

    return render_template("catalog_form.html", bikes=result, page=page)


if __name__ == "__main__":
    page = 1
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=65010)
