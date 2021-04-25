import datetime
import json
from json import JSONEncoder

class Tweet:
    def __init__(self, text):
        self.text = text
        self.likes = 0
        self.date = str(datetime.datetime.now())

    def jsonify(self):
        newTweet = {"tweet":self.text, "likes":self.likes, "date":self.date}
        return newTweet

