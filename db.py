import pymongo
from flask import request

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/yourdb'  # Replace with your MongoDB URI
mongo = PyMongo(app)


client = pymongo.MongoClient('mongodb://127.0.0.1:27017/mydatabase')
userdb = client['user']
users = userdb.customers



def insert_data():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		password = request.form['pass']
		age = request.form['age']
		gender = request.form['gender']

		reg_user = {}
		reg_user['name'] = name
		reg_user['email'] = email
		reg_user['password'] = password
		reg_user['age'] = age
		reg_user['gender'] = gender
		

		if users.find_one({"email":email}) == None:
			users.insert_one(reg_user)
			return True
		else:
			return False


def check_user():

	if request.method == 'POST':
		email = request.form['email']
		password = request.form['pass']

		user = {
			"email": email,
			"password": password
		}

		user_data = users.find_one(user)
		if user_data == None:
			return False, ""
		else:
			return True, user_data["name"]
		
