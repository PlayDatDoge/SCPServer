
#Imports!
from json import tool
from logging import exception
from types import TracebackType
from flask import flash, redirect, url_for, render_template, request,session  
from .models import db, User,login_manager
import flask_login
from flask_login import login_user, login_required, logout_user , current_user
from flask import current_app as app
from flask import flash
from flask_sqlalchemy import SQLAlchemy
import traceback


@app.route('/index')
@app.route('/')
def index():
	if not flask_login.current_user.is_authenticated:
		if 'user' in session:	
			if logged_user := User.query.filter_by(username=session['user']).first():
				login_user(logged_user)
				session['theme'] = current_user.theme
				return render_template('index.html')
		else:
			return redirect(url_for('login'))
	return render_template('index.html')


@app.route('/logout')
@login_required
def logout():
	session.pop('user', None)
	session.pop('theme', None)
	session.pop('database', None)
	logout_user()
	return redirect(url_for('login'))	
								

@app.route('/login', methods=['POST', 'GET'])
def login():
	if not flask_login.current_user.is_authenticated:
		if 'user' in session:
			if logged_user := User.query.filter_by(username=session['user']).first():
				login_user(logged_user)
				session['theme'] = current_user.theme
				return redirect(url_for('index'))
		
		if request.method == 'POST':
			username12 = request.form['username']
			password = request.form['password']
			if logged_user := User.query.filter_by(username=username12).first():
				if logged_user.validate_password(password):
					session['user'] = logged_user.username
					session['theme'] = logged_user.theme
					login_user(logged_user)
					print(current_user)
					return redirect(url_for('index'))

		return render_template('Login.html')
	return redirect(url_for('index'))


@app.route('/register', methods=['POST', 'GET'])
def register():
	error = None
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		email = request.form["email"]
		if not  User.query.filter_by(username=username).first() and not User.query.filter_by(email=email).first() :
			db.session.add(User(username=username, password=password, email=email))
			db.session.commit()
			return redirect(url_for('login'))
		else:
			error = 'Invalid credentials'
			flash('invalid credentials,Either Email Or username are taken')
	return render_template('register.html',error=error)




@app.route('/userpref',methods=['POST', 'GET'])
@login_required
def userpref():
	if request.method == 'POST':
		if 'cbox' in request.form:
			print(current_user.theme)
			if current_user.theme == 'theme':
				current_user.theme = 'dark_theme'
			elif current_user.theme == 'dark_theme':
				current_user.theme = 'theme'
			session['theme'] = current_user.theme
		db.session.commit()
	return render_template('userpref.html')


@app.route('/tools',methods=['POST', 'GET'])
@login_required
def tools():
	if current_user.user_clearnace == 1:
		print("hopsder")
		return render_template('index.html')


	return render_template('tools.html')

@app.route('/enodo',methods=['POST', 'GET'])
@login_required
def enodo():
	if current_user.user_clearnace == 2:
		print("hopsder")
		return render_template('index.html')


	return render_template('enodo.html')

@login_manager.unauthorized_handler
def unauthorized():
	return redirect(url_for('login'))


@app.errorhandler(404)
def error_handler(error):
	print(error)
	return render_template("404.html")



@app.route('/sitetools',methods=['POST', 'GET'])
@login_required
def sitetools():

	return render_template('sitetools.html')



	

