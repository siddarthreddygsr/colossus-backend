from flask import Flask, jsonify, request, session, redirect,render_template, url_for
from passlib.hash import pbkdf2_sha256
import time
import smtplib, ssl
from app import db, client
import uuid


smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "bot.ratemyuniversity@gmail.com"
password = "CringeMax#479"

# Create a secure SSL context
context = ssl.create_default_context()
server = smtplib.SMTP(smtp_server,port)
server.ehlo()
server.starttls(context=context) # Secure the connection
server.ehlo()
# server.login(sender_email, password)

class User:
	def start_session(self, user):
		del user['password']
		session['logged_in'] = True
		session['user'] = user
		return jsonify(user), 200

	def signup(self):

		verification_code = str(uuid.uuid4().hex)
		# Create the user object
		user = {
		"_id": uuid.uuid4().hex,
		"name": request.form.get('name'),
		"email": request.form.get('email'),
		"password": request.form.get('password'),
		"token_generation_epoch": int(time.time())
		}

		# Encrypt the password
		user['password'] = pbkdf2_sha256.encrypt(user['password'])

		# Check for existing email address
		if db.users.find_one({ "email": user['email'] }):
			return jsonify({ "error": "Email address already in use" }), 400

		return jsonify({ "error": "Signup failed" }), 400

	def signout(self):
		session.clear()
		return redirect('/')
	

	def login(self):

		user = db.users.find_one({
		"email": request.form.get('email')
		})

		verified = user['verified'] if user else False

		if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
			if verified:
				return self.start_session(user)
			else:
				return jsonify({ "error": "Email address not verified" }), 400
		
		return jsonify({ "error": "Invalid login credentials" }), 401
	
	def email_verification(self):
		return render_template('email_verification.html')

	def search_unique_email(self):
		search = request.form.get('searchTerm')
		search = "^" + search + ".*"
		user = db.users.find(
			{
				"email" : { "$regex": search, "$options": "i" }
			}
		)
		return jsonify(list(user))
	
	def adduni(self):
		return render_template('adduni.html')

	def adduni_image(self):
		if 'uni-image' in request.files:
			uni_image = request.files['uni-image']
			client.save_file(uni_image.filename, uni_image)
			db.unapproved_universities.insert({"university": request.form.get('university'), "image": uni_image.filename})

		return 'Done!'