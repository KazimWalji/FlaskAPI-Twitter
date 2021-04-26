import datetime
import json
from json import JSONEncoder


class Tweet:
    def __init__(self, text):
        self.text = text
        self.likes = 0
        month = datetime.datetime.today().month
        day = datetime.datetime.today().day
        time = datetime.datetime.now().strftime("%H:%M:%S")
        self.date = {"month": month, "day": day, "time": time}

    def jsonify(self):
        newTweet = {"tweet": self.text, "likes": self.likes, "date": self.date}
        return newTweet
