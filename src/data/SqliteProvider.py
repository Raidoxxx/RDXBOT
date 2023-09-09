from abc import ABC
import sqlite3

from src.data.DataProvider import DataProvider


class SqliteProvider(DataProvider, ABC):
    def __init__(self):
        super().__init__()
        self.cursor = None
        self.connection = None

    def connect(self, param):
        self.connection = sqlite3.connect(param)
        self.cursor = self.connection.cursor()

    def getUser(self, id):
        self.cursor.execute(f"SELECT * FROM users WHERE id = {id}")
        return self.cursor.fetchall()

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
