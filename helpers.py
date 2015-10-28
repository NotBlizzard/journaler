from pymongo import MongoClient
from bson.objectid import ObjectId
import bcrypt
import time
import datetime

client = MongoClient()
db = client['journaler']
posts = db['posts']
users = db['users']

def register_account(username, password):
	data = users.find_one({'username': username})
	if data:
		return False

	hashed = bcrypt.hashpw(bytes(password, encoding='UTF-8'), bcrypt.gensalt())
	users.insert_one({"username": username, "password": hashed})
	return True

def login_user(username, password):
	data = users.find_one({"username": username})
	if not data:
		return False

	if bcrypt.hashpw(bytes(password, encoding='UTF-8'), data['password']) == data['password']:
		return True
	else:
		return False

def get_post(id, username):
	post =  posts.find_one({"_id": ObjectId(id)})
	if not post:
		return False

	if post['username'] == username:
		return post
	else:
		return False

def get_posts(username):
	p = []
	for post in posts.find({"username": username}):
		p.append(post)

	return p

def make_post(username, content):
	t = int(time.time())
	posts.insert_one({"username": username, "content": content, "timestamp": t, "date": datetime.datetime.fromtimestamp(t).strftime("%Y-%m-%d")})
	return posts.find_one({"date": t})
