from abc import ABC

import mysql.connector

from src.data.DataProvider import DataProvider


class MySqlProvider(DataProvider, ABC):
    def __init__(self):
        super().__init__()
        self.cursor = None
        self.connection = None
        self.data = self.load_data()

    def load_data(self):
        self.data = {}
        return self.data

    def getUser(self, id):
        self.cursor.execute(f"SELECT * FROM users WHERE id = {id}")
        return self.cursor.fetchall()

    def connect(self, host, user, password, schema):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=schema
        )

        self.cursor = self.connection.cursor()

    def get_data(self):
        return self.data

    def get(self, key):
        self.cursor.execute(f"SELECT * FROM {key}")
        return self.cursor.fetchall()

    def set(self, key, value):
        self.cursor.execute(f"INSERT INTO {key} VALUES {value}")

    def remove(self, key):
        self.cursor.execute(f"DELETE FROM {key}")

    def update(self, key, value):
        self.cursor.execute(f"UPDATE {key} SET {value}")

    def save_data(self, data):
        self.connection.commit()