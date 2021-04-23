from flask import Flask
from flask_restful import Api, Resource
from flask import jsonify
app = Flask(__name__)


@app.route("/users", methods=['GET', 'POST'])
def users():
    return jsonify({"Name": "kazim"})


if __name__ == "__main__":
    app.run()