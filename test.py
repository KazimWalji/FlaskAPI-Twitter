import requests
import datetime
from app import db

# db.drop_all()
# db.create_all()
Base = 'http://127.0.0.1:5000/follow/Test/Admin'
# addUser = "hello"
response = requests.post(Base)
print(response.json())

