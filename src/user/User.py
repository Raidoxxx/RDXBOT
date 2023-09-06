from src.data.DataManager import DataManager


class User(id(int)):
    def __int__(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def get_data(self):
        return DataManager().get_data().getUser(self.id)

    def getStandoff(self):
        return self.get_data().get("standoff-id")

    def setStandoff(self, id):
        self.get_data().set("standoff-id", id)

