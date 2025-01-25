class UserManager:
    def __init__(self):
        self.users = {}

    def create_user(self, userid, email):
        if userid in self.users:
            return False
        self.users[userid] = {"email": email}
        return True

    def get_user(self, userid):
        return self.users.get(userid)
