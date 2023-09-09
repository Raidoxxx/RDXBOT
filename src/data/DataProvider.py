import abc


class DataProvider(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def getUser(self, id):
        pass

    @abc.abstractmethod
    def get_data(self):
        pass

    @abc.abstractmethod
    def get(self, key):
        pass

    @abc.abstractmethod
    def set(self, key, value):
        pass

    @abc.abstractmethod
    def remove(self, key):
        pass

    @abc.abstractmethod
    def update(self, key, value):
        pass

    @abc.abstractmethod
    def save_data(self, data):
        pass
