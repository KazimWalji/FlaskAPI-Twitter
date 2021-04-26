from flask import Flask
from flask import jsonify, make_response
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy
from Tweet import Tweet
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship
import json
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    tweets = db.Column(MutableList.as_mutable(db.PickleType),
                                    default=[])
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def follow(self, user):
        if user is None:
            message = user + " doesn't exist"
            abort(404, message=message)
            return
        if not self.is_following(user):
            self.followed.append(user)

    def jsonify(self):
        followersList = self.followed.all()
        newList = []
        for f in followersList:
            newList.append({"followers": [], "username": f.username, "password": f.password, "tweets": tweetsJsonify(f.tweets)})
        data = {"followers": newList, "username": self.username, "password": self.password, "tweets": tweetsJsonify(self.tweets)}
        return data

    def __repr__(self):
        return '<User %r>' % self.username

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0



class apiUser(Resource):
    def post(self, username, password):
        print("username:", username)
        exists = (User.query.filter_by(username=username).first())
        if exists is not None:
            abort(404,message="User exists")
        tempUser = User(username=username, password=password, tweets=[])
        db.session.add(tempUser)
        db.session.commit()
        print(tempUser.jsonify())
        return jsonify(tempUser.jsonify())

    def get(self, username, password):
        user = (User.query.filter_by(username=username, password=password).first())
        if user is None:
            abort(404,message="User doesn't exist")
        else:
            print(user.jsonify())
            return jsonify(user.jsonify())

class getTweets(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return jsonify(tweetsJsonify(user.tweets))
        else:
            return jsonify("tweets not available")

class Followers(Resource):
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            abort(404, message="User doesn't exist")
        dict = user.jsonify()
        return dict["followers"]
class addFollower(Resource):
    def post(self, username, otherName):
        user = User.query.filter_by(username=username).first()
        other = User.query.filter_by(username=otherName).first()
        if user is None or other is None:
            abort(404, message="User doesn't exist")
        user.follow(other)
        db.session.commit()
        return jsonify([True])


class addTweets(Resource):
    def post(self, username, text):
        tweet = Tweet(text)
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify([False])
        user.tweets.append(tweet)
        db.session.add(user)
        db.session.commit()
        return jsonify([True])

def tweetsJsonify(list):
    newTweets = []
    for tweet in list:
        newTweets.append(tweet.jsonify())
    return newTweets
@app.route("/getUsers")
def getUsers():
    allUsers = User.query.all()
    data = {}
    for user in allUsers:
        data[user.username] = user.jsonify()
    if data == {}:
        print("no users")
        abort(404, message="No data")
        return
    return jsonify(data)


api.add_resource(apiUser, '/user/<string:username>/<string:password>')
api.add_resource(getTweets, '/tweets/<string:username>')
api.add_resource(addTweets, '/tweets/<string:username>/<string:text>')
api.add_resource(Followers, '/followers/<string:username>', methods=['GET'])
api.add_resource(addFollower, '/follow/<string:username>/<string:otherName>', methods=['POST'])
if __name__ == "__main__":
    app.run(debug=True)
