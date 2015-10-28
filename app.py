from flask import Flask, render_template, request, session, redirect, url_for
from helpers import register_account, get_posts, make_post, get_post, login_user
import datetime
import re

app = Flask(__name__)

app.debug = True
app.secret_key = 'foobar'

@app.route("/")
def root():
	if 'username' in session:
		return redirect(url_for('home'))

	return render_template("root.html")

@app.route("/home")
def home():
	if not 'username' in session:
		return redirect("/")

	posts = get_posts(session['username'])

	return render_template("home.html", posts=posts)

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	else:
		username = request.form["username"].lower()
		password = request.form["password"]

		reg = register_account(username, password)
		if reg == True:
			session['username'] = username
			return redirect(url_for('home'))
		else:
			return render_template("register.html", error="Username is already taken.")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		username = request.form['username'].lower()
		password = request.form['password']
		log = login_user(username, password)
		if log == True:
			session['username'] = username
			return redirect(url_for('home'))
		else:
			return render_template("login.html", error="Wrong username and/or password.")

@app.route("/logout")
def logout():
	session['username'].pop()
	return redirect("/")

@app.route("/new", methods=["GET", "POST"])
def new():
	if request.method == 'GET':
		if not 'username' in session:
			return redirect("/")

		return render_template("new.html")
	else:
		content = request.form["content"]
		post = make_post(session['username'], content)
		return redirect(url_for("home"))

@app.route("/<id>")
def show(id):
	post = get_post(id, session['username'])
	if post == False:
		return render_template('show.html', error='You can\'t view this entry.')
	else:
		return render_template('show.html', post=post)


if __name__ == '__main__':
	app.run()
