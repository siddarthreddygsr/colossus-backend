from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo
import json

with open('config.json', 'r') as configurations:
    config = json.load(configurations)

app = Flask(__name__)
app.secret_key = config.get('FLASK_SECRET_KEY')
print(config.get('FLASK_SECRET_KEY'))
# Database
client = pymongo.MongoClient('localhost', 27017)
db = client.user_login_system


# Decorators
# def login_required(f):
#   @wraps(f)
#   def wrap(*args, **kwargs):
#     if 'logged_in' in session:
#       return f(*args, **kwargs)
#     else:
#       return redirect('/')
  
#   return wrap