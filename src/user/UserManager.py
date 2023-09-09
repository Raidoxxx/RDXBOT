from src.data.DataManager import DataManager
from src.user.User import User


class UserManager:
    def __init__(self):
        self.users = []
        data = DataManager().get_data().get("users")

        for userdata in data:
            user = User(userdata["id"])
            self.register(user)

    def register(self, User):
        if User not in self.users:
            self.users.append(User)
            return True

        return False

    def unregister(self, User):
        if User in self.users:
            self.users.remove(User)
            return True

        return False

    def get_user(self, id):
        for user in self.users:
            if user.get_id() == id:
                return user

        return None

    def get_users(self):
        return self.users

    def exists(self, id):
        for user in self.users:
            if user.get_id() == id:
                return True

        return False
