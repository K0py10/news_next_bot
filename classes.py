class post_from_ds:
    def __init__(self, channel, text):
        self.channel = channel
        self.text = text

class post:
    def __init__(self, channel, text, vector):
        self.channel = channel
        self.text = text
        self.vector = vector