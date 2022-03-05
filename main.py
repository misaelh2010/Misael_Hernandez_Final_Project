import hashlib
import datetime
import time
import flask
from flask import jsonify
from flask import request, make_response
from sql import create_connection
from sql import execute_read_query
from sql import execute_query
from datetime import datetime

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


@app.route('/trip', methods=['POST'])
def add_trip():
    request_data = request.get_json()
     #i had to modify the destinationid request so that it would take the info from the body section in postman and post it to the table
    strid = request_data['destinationid']     
    newdestinationid = str(strid)
    newtripname = request_data['tripname']
    newtransportation = request_data['transportation']
    #i had to change the datetime variable into a str so that it would get inserted into the table for both startdate and enddate
    startdate = (request_data['startdate'])  
    newstartdate = str(datetime.strptime(startdate, '%m-%d-%Y').date())
    enddate = request_data['enddate']
    newenddate = str(datetime.strptime(enddate, '%m-%d-%Y').date())
    
    #connection to db and sql query to insert into table
    conn = create_connection('cis3368.cygrl7flcnjt.us-east-2.rds.amazonaws.com', 'admin', 'Amaterasu24!', 'cis3368db')
    sql = "INSERT INTO trip (destinationid, tripname, transportation, startdate, enddate) VALUES ('"+newdestinationid+"','"+newtripname+"','"+newtransportation+"','"+newstartdate+"','"+newenddate+"')"
    execute_query(conn, sql)
    return 'Trip added successfully'





app.run()