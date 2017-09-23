from flask import Flask, render_template, json, request
from pymongo import MongoClient
import json
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
import pymongo

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
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST','GET'])
def signUp():
    users.insert_one(request.form.to_dict())
    #run google calendar authentification
    google()

@app.route('/google')
def google():
    #google code for calendar goes here, could add success screen after sign in
    
   

if __name__ == "__main__":
    app.run()
    #app.run(port=5002)
