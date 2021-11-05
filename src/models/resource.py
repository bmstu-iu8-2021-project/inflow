class Resource:
    def __init__(self, id, label, link):
        self.id = id
        self.label = label
        self.link = link

    def __str__(self):
        return "resource[{}]({}, {})".format(self.id, self.label, self.link)

    def __repr__(self):
        return str(self)
