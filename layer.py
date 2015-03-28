from flask import Flask, request
import requests
import json
from db import check_arguments

app = Flask(__name__)


def get_session_url(url_part):
    return "http://localhost:65011/" + url_part


def get_users_url(url_part):
    return "http://localhost:65012/" + url_part


def get_bikes_url(url_part):
    return "http://localhost:65013/" + url_part


def check_connection(login, code):
    url = get_session_url("check_connection?login={0}&code={1}".format(login, code))
    result = requests.get(url).json()
    return 'ok' in result


@app.route("/login")
def login():
    try:
        if not check_arguments(['login', 'password'], request.args):
            raise Exception('Bad arguments')

        login = request.args.get('login')
        password = request.args.get('password')

        url = get_session_url("login?login={0}&password={1}".format(login, password))
        result = requests.get(url)
        return result.text

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/logout")
def logout():
    try:
        if not check_arguments(['login', 'code'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get("login")
        code = request.args.get("code")

        url = get_session_url("logout?login={0}&code={1}".format(login, code))
        result = requests.get(url)
        return result.text

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/me")
def me():
    try:
        if not check_arguments(['login', 'code'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get('login')
        code = request.args.get('code')

        if check_connection(login, code):
            url = get_users_url("me") + "?login={0}".format(login)
            result = requests.get(url)
            return result.text

        raise Exception("Access denied")

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/add_user", methods=['POST'])
def add_user():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'first', 'second', 'age', 'city',
                                'like', 'email', 'my', 'password'], data_json):
            raise Exception("Bad arguments")

        login = data_json['login']
        password = data_json['password']

        if not (login and password):
            raise Exception("Login and password can't be empty")

        url = get_users_url("add_login")
        data = {'login': login, 'password': password}
        headers = {'Content-type': 'application/json'}

        result = requests.post(url, data=json.dumps(data), headers=headers).json()
        if 'error' in result:
            raise Exception(result['error'])

        first = data_json['first']
        second = data_json['second']
        age = data_json['age']
        city = data_json['city']
        email = data_json['email']
        like = data_json['like']
        my = data_json['my']

        url = get_users_url("add_user")
        data = {'login': login, 'first': first, 'second': second, 'age': age,
                'city': city, 'email': email, 'like': like, 'my': my}

        result = requests.post(url, data=json.dumps(data), headers=headers)
        return result.text

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/remove_user", methods=['DELETE'])
def remove_user():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'code'], data_json):
            raise Exception("Bad arguments")

        login = data_json['login']
        code = data_json['code']

        if check_connection(login, code):
            url = get_users_url("remove_login")
            data = {'login': login}
            headers = {'Content-type': 'application/json'}
            result = requests.delete(url, data=json.dumps(data), headers=headers).json()
            if 'error' in result:
                raise Exception(result['error'])

            url = get_users_url("remove_user")
            result = requests.delete(url, data=json.dumps(data), headers=headers).json()
            if 'error' in result:
                raise Exception(result['error'])

            url = get_session_url("logout?login={0}&code={1}".format(login, code))
            result = requests.get(url)

            return result.text

        raise Exception("Access denied")

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/get_user_info")
def get_user_info():
    try:
        if not check_arguments(['login', 'code'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get('login')
        code = request.args.get('code')

        if check_connection(login, code):
            url = get_users_url("login_to_id") + "?login={0}".format(login)
            result = requests.get(url).json()
            if 'error' in result:
                raise Exception(result['error'])

            url = get_users_url("user/{0}".format(result['id']))
            result = requests.get(url)

            return result.text

        raise Exception("Access denied")

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/update_user_info", methods=['PUT'])
def update_user_info():
    try:
        data_json = request.get_json()
        if not check_arguments(['login', 'first', 'second', 'age', 'city',
                                'like', 'email', 'my', 'code'], data_json):
            raise Exception("Bad arguments")

        login = data_json['login']
        code = data_json['code']

        if check_connection(login, code):
            first = data_json['first']
            second = data_json['second']
            age = data_json['age']
            city = data_json['city']
            email = data_json['email']
            like = data_json['like']
            my = data_json['my']

            url = get_users_url("update_user")
            data = {'login': login, 'first': first, 'second': second, 'age': age,
                    'city': city, 'email': email, 'like': like, 'my': my}
            headers = {'Content-type': 'application/json'}

            result = requests.put(url, data=json.dumps(data), headers=headers)

            return result.text

        raise Exception("Access denied")

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/like_bikes")
def like_bikes():
    try:
        if not check_arguments(['login', 'code', 'id'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get('login')
        code = request.args.get('code')

        if check_connection(login, code):
            _id = request.args.get("id")
            url = get_users_url("user/{0}".format(_id))

            result = requests.get(url).json()
            if 'error' in result:
                raise Exception(result['error'])

            answer = []
            bikes = result['like_bikes'].split(",")
            for bike in bikes:
                url = get_bikes_url("short_info?id={0}".format(bike))
                result = requests.get(url).json()
                if 'error' in result:
                    raise Exception(result['error'])
                answer.append(result)

            return json.dumps(answer)

        raise Exception("Access denied")

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/my_bikes")
def my_bikes():
    try:
        if not check_arguments(['login', 'code', 'id'], request.args):
            raise Exception("Bad arguments")

        login = request.args.get('login')
        code = request.args.get('code')

        if check_connection(login, code):
            url = get_users_url("login_to_id") + "?login={0}".format(login)
            result = requests.get(url).json()
            if 'error' in result:
                raise Exception(result['error'])

            _id = request.args.get("id")
            if int(_id) != result['id']:
                raise Exception("Permission denied")

            url = get_users_url("user/{0}".format(_id))
            result = requests.get(url).json()
            if 'error' in result:
                raise Exception(result['error'])

            answer = []
            bikes = result['my_bikes'].split(",")
            for bike in bikes:
                url = get_bikes_url("full_info?id={0}".format(bike))
                result = requests.get(url).json()
                if 'error' in result:
                    raise Exception(result['error'])
                answer.append(result)

            return json.dumps(answer)

        raise Exception("Access denied")

    except Exception as e:
        return json.dumps({'error': str(e)})


@app.route("/catalog")
def catalog():
    try:
        if not check_arguments(['page'], request.args):
            raise Exception("Bad arguments")

        url = get_bikes_url("get_all_bikes?page={0}".format(request.args.get('page')))

        result = requests.get(url)

        return result.text

    except Exception as e:
        return json.dumps({'error': str(e)})


if __name__ == "__main__":
    app.run(debug=True, port=65014)
