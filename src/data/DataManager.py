import json
import os

from src.data.DataProvider import DataProvider
from src.data.JsonProvider import JsonProvider
from src.data.MySqlProvider import MySqlProvider


class DataManager:
    def __init__(self):
        self.dataProvider = DataProvider()
        self.data = self.load_data()

    def get_data(self):
        return self.dataProvider.get_data()

    def get_data_provider(self):
        return self.dataProvider

    def load_data(self):
        if not os.path.exists("config.yml"):
            self.data = JsonProvider().load_data()
        else:
            with open("config.yml", 'r') as file:
                config = json.load(file)

        match config["database"]["type"]:
            case "json":
                self.data = JsonProvider().load_data()
            case "mysql":
                self.data = MySqlProvider()
                self.data.connect(
                    config["database"]["host"],
                    config["database"]["user"],
                    config["database"]["password"],
                    config["database"]["schema"]
                )