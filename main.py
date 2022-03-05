import hashlib
import datetime
import time
import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_read_query
from sql import execute_query

#setting up the application
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show error in browser


#this app route is going to be for the login, it is going to be based on the one we saw in class
#i had to find a tool online to produce the hashed value of the password
#https://passwordsgenerator.net/sha256-hash-generator/
#password 'Rengoku' hashed
masterPassword = "06be480051ca657dc38fc0dfc80766d1d7da8a4cf6b48665fc4ce02e87c29455"
masterUsername = 'Misael'


#this get method is going to be the login authentication needed right before the page is accessed
@app.route('/', methods=['GET'])
def auth_login():
    if request.authorization:
        encoded=request.authorization.password.encode() #unicode encoding
        hashedResult = hashlib.sha256(encoded) #hashing
        if request.authorization.username == masterUsername and hashedResult.hexdigest() == masterPassword:
            return '<h1> WElLCOME TO VACATION PLANNER </h1>'
    return make_response('COULD NOT VERIFY CREDENTIALS!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})




app.run()