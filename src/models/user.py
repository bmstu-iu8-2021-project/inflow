class User:
    def __init__(self, id, login, password):
        self.id = id
        self.login = login
        self.password = password

    def __str__(self):
        return "tag[{}]({}, {})".format(self.id, self.login, self.password)

    def __repr__(self):
        return str(self)
