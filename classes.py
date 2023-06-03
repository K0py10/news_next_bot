class post:
    def __init__(self, id, channel, text, lem_text):
        self.id = id
        self.channel = channel
        self.text = text
        self.lem_text = lem_text

class channel:
    def __init__(self, id, name, last_message):
        self.id = id
        self.name = name
        self.last_message = last_message