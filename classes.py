class post:
    def __init__(self, id, channel, lem_text):
        self.id = id
        self.channel = channel
        self.lem_text = lem_text

class channel:
    def __init__(self, id, name, last_message):
        self.id = id
        self.name = name
        self.last_message = last_message

class message:
    def __init__(self, chat, id, text):
        self.chat = chat
        self.id = id
        self.text = text