import json
import os
from abc import ABC

from src.data.DataProvider import DataProvider


class JsonProvider(DataProvider, ABC):
    def __init__(self):
        super().__init__()
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists("data.json"):
            self.data = {}
            self.save_data(self.data)
        else:
            with open("data.json", 'r') as file:
                self.data = json.load(file)

        return self.data

    def getUser(self, id):
        return self.data.get(id)

    def get_data(self):
        return self.data

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value

    def remove(self, key):
        self.data.pop(key)

    def update(self, key, value):
        self.data[key] = value

    def save_data(self, data):
        with open("config.json", 'w') as file:
            json.dump(data, file)
