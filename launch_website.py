from flask import Flask, render_template, json, request
from pymongo import MongoClient
import json
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from bson.objectid import ObjectId
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from signal import signal, SIGPIPE, SIG_DFL
import ast

import datetime

app = Flask(__name__)
mongo=PyMongo(app)
app.debug=True
connection = MongoClient("mongodb://ds147544.mlab.com:47544/")
db = connection["userdatabase"]
users=db.users
db.authenticate(name="nikosm",password="Netherlands1")

@app.route('/')
def main():
    return render_template('index.html')
# @app.route('/showSignUp')
# def showSignUp():
#     return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
	ans=ast.literal_eval(request.data)
	users.insert_one(ans)
	
	return "done"

# @app.route('/google')
# def google():
#        #google calendar code
#     home_dir = os.path.expanduser('~')
#     credential_dir = os.path.join(home_dir, '.credentials')
#     credential_path = os.path.join(credential_dir,
#                                    'calendar-python-quickstart.json')
#     store = Storage(credential_path)
#     credentials = store.get()
#     http = credentials.authorize(httplib2.Http())
#     service = discovery.build('calendar', 'v3', http=http)

#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Succesful authentification')
#    # http.close()
#     return "Congratulations!Succesful authentification"

if __name__ == "__main__":
    app.run()
    
    #app.run(port=5002)

