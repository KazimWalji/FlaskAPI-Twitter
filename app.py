from flask import Flask
from flask import jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from Tweet import Tweet
from sqlalchemy.ext.mutable import MutableList

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    tweets = db.Column(MutableList.as_mutable(db.PickleType),
                                    default=[])

    def __repr__(self):
        return '<User %r>' % self.username



class apiUser(Resource):
    def post(self, username, password):
        print("username:", username)
        exists = (User.query.filter_by(username=username).first())
        if exists is not None:
            return jsonify([False])
        tempUser = User(username=username, password=password, tweets=[])
        db.session.add(tempUser)
        db.session.commit()
        return jsonify([True])

    def get(self, username, password):
        user = (User.query.filter_by(username=username, password=password).first())
        if user is not None:
            return jsonify([True])
        else:
            return jsonify([False])


@app.route("/getUsers")
def getUsers():
    allUsers = User.query.all()
    data = {}
    for user in allUsers:
        data[user.username] = {"username": user.username, "password": user.password, "tweets":user.tweets}
    return jsonify(data)


api.add_resource(apiUser, '/user/<string:username>/<string:password>')
if __name__ == "__main__":
    app.run(debug=True)
