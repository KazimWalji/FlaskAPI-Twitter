import datetime
import json
from json import JSONEncoder


class Tweet:
    def __init__(self, text):
        self.text = text
        self.likes = 0
        month = datetime.datetime.today().month
        day = datetime.datetime.today().day
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        self.date = {"month": month, "day": day, "hour":hour, "min":minute}

    def jsonify(self):
        newTweet = {"text": self.text, "likes": self.likes, "date": self.date}
        return newTweet
