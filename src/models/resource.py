class Resource:
    def __init__(self, id, title, link):
        self.id = id
        self.title = title
        self.link = link

    def __str__(self):
        return "resource[{}]({}, {})".format(self.id, self.title, self.link)

    def __repr__(self):
        return str(self)
