import datetime

class Tweet:
    def __init__(self, text):
        self.text = text
        self.likes = 0
        self.date = str(datetime.datetime.now())

    def __init__(self):
        self.text = ""
        self.likes = 0
        self.date = str(datetime.datetime.now())
