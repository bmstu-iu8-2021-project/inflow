class Tag:
    def __init__(self, id, label, color):
        self.id = id
        self.label = label
        self.color = color

    def __str__(self):
        return "tag[{}]({}, {})".format(self.id, self.label, self.color)

    def __repr__(self):
        return str(self)

