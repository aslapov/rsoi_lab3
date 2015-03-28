# -*- coding: utf-8 -*-


class ConnectionInfo:
    def __init__(self, login_str, code_str):
        self.login = login_str
        self.code = code_str

    def __eq__(self, other):
        return self.login == other.login and self.code == other.code


class Connections:
    def __init__(self):
        self.connections = []

    def add(self, item):
        self.connections.append(item)

    def remove(self, login, code):
        for element in self.connections:
            if element.login == login and element.code == code:
                self.connections.remove(element)
                return True

        return False

    def find(self, item):
        for element in self.connections:
            if element == item:
                return True

        return False