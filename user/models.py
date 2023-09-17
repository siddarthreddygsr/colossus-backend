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
	def vc(self):
		try:
			a+belo
		except:
			return render_template('email_verification.html')

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
		"verification_token": verification_code,
		"token_generation_epoch": int(time.time()),
		"verified": False
		}

		# Encrypt the password
		user['password'] = pbkdf2_sha256.encrypt(user['password'])

		# Check for existing email address
		if db.users.find_one({ "email": user['email'] }):
			return jsonify({ "error": "Email address already in use" }), 400



		#verify email address
		

		# Try to log in to server and send email
		if db.users.insert_one(user):
			print('Sending email')
			print("1")
			try:
				receiver_email = user['email']
				print(receiver_email)
				message =  """\
				Subject: %s

				%s
				""" % ("email verification", "Please verify your email address by clicking on the link below:\n\nhttp://127.0.0.1:5000/confirm_email/" + verification_code)
				server.sendmail(sender_email, receiver_email, message)
				print('Email sent')
				return redirect('/email_verification/')
			except smtplib.SMTPSenderRefused:
				try:
					server.quit()
				except:
					print('Starting email server')
					server.login(sender_email, password)
				try:
					receiver_email = user['email']
					print(receiver_email)
					message =  """\
					Subject: %s

					%s
					""" % ("email verification", "Please verify your email address by clicking on the link below:\n\nhttp://127.0.0.1:5000/confirm_email/" + verification_code)
					server.sendmail(sender_email, receiver_email, message)
					print('Email sent')
					return redirect('/email_verification/')
				except Exception as e:
					print(e)
					return jsonify({ "error": "Error sending email" }), 500
			except Exception as e:
				# Print any error messages to stdout
				print("error occured: ", e)
				return jsonify({ "error": "Error sending email" }), 400
			print("redirecting")

		return jsonify({ "error": "Signup failed" }), 400
	
	def confirm_email(self, token):
		user = db.users.find_one({
		"verification_token": token
		})

		if not user:
			return jsonify({ "error": "Invalid verification token" }), 400
		print(int(time.time()) - user['token_generation_epoch'])
		if int(time.time()) - user['token_generation_epoch'] > 86400:
			return jsonify({ "error": "Verification token expired" }), 400

		user['verified'] = True
		db.users.replace_one({ "_id": user['_id'] }, user)
		print(user)
		return redirect('/')

	def signout(self):
		session.clear()
		return redirect('/')
	
	def sign_up(self):
		return render_template('signup.html')
	

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