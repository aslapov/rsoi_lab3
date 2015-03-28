# -*- coding: utf-8 -*-
import sqlite3


def check_arguments(what, where):
    if not where:
        return False

    for i in what:
        if not i in where:
            return False

    return True


class DBWorker:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.db_name = "bikes.db"
        self.records_per_page = 2

    def execute_query(self, query):
        self.connection = sqlite3.connect(self.db_name)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        records = self.cursor.execute(query).fetchall()
        self.connection.commit()
        self.connection.close()
        return records

    def execute_and_return_json(self, query):
        records = self.execute_query(query)
        records_json = [dict(rec) for rec in records]
        return records_json

    def insert_into_login_data_table(self, login, password):
        query = "INSERT INTO login_data VALUES ('{0}', '{1}')".format(login, password)
        self.execute_query(query)

    def delete_from_login_data_table(self, login):
        query = "DELETE FROM login_data WHERE login='{0}'".format(login)
        return self.execute_query(query)

    def insert_into_users_data_table(self, login, fname, sname, age, city, email, like, my):
        query = "INSERT INTO users_data VALUES (NULL, '{0}', '{1}', '{2}', {3}, '{4}', '{5}', '{6}', '{7}')".\
                format(login, fname, sname, age, city, email, like, my)
        self.execute_query(query)

    def delete_from_users_data_table(self, login):
        query = "DELETE FROM users_data WHERE login='{0}'".format(login)
        return self.execute_query(query)

    def update_users_data_table(self, login, fname, sname, age, city, email, like, my):
        query = "UPDATE users_data set firstname='{0}', secondname='{1}', age='{2}', " \
                "city='{3}', email='{4}', like_bikes='{5}', my_bikes='{6}' " \
                "where login='{7}'".format(fname, sname, age, city, email, like, my, login)
        return self.execute_query(query)

    def confirm_login_data(self, login, password):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        query = "SELECT * FROM login_data WHERE login='{0}' AND password='{1}'".format(login, password)
        records = self.execute_query(query)
        return len(records) > 0

    def get_user_data_by_id(self, _id):
        query = "SELECT firstname, secondname, age, city, email, like_bikes, my_bikes" \
                " FROM users_data WHERE id={0}".format(_id)
        return self.execute_and_return_json(query)

    def get_user_data_by_login(self, login):
        query = "SELECT firstname, secondname, age, city, email, like_bikes, my_bikes" \
                " FROM users_data WHERE login='{0}'".format(login)
        return self.execute_and_return_json(query)

    def get_id_by_login(self, login):
        query = "SELECT id FROM users_data WHERE login='{0}'".format(login)
        return self.execute_and_return_json(query)

    def get_short_bike_info_by_id(self, _id):
        query = "SELECT firm, model, description FROM bikes_data WHERE id={0}".format(_id)
        return self.execute_and_return_json(query)

    def get_full_bike_info_by_id(self, _id):
        query = "SELECT firm, model, color, cost, description FROM bikes_data WHERE id={0}".format(_id)
        return self.execute_and_return_json(query)

    def get_all_bikes(self, page, count_per_page):
        offset = (int(page)-1) * count_per_page
        query = "SELECT firm, model, color, cost, description FROM bikes_data " \
                "LIMIT {0} OFFSET {1}".format(count_per_page, offset)
        return self.execute_and_return_json(query)
