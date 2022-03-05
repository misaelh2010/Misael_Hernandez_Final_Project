import hashlib
import datetime
import time
import flask#, werkzeug
from flask import jsonify, make_response
from flask import request, make_response
from sql import create_connection
from sql import execute_read_query
from sql import execute_query
from datetime import datetime
#from werkzeug.exceptions import HTTPException

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

#for this endpoint i havent decided yet if it will be needed for sprint 2, so i will leave it like this for now 
#and reevaluate during sprint2
#this endpoint is going to get the trip by its destinationid
#@app.route('/trip', methods=['GET'])
#def get_trip():
#    if 'destinationid' in request.args: #only if an id is provided as an argument, proceed
#        destinationid = int(request.args['destinationid'])
##    else:
 #       return 'ERROR: No ID provided!'
 #   
 #   #connection to db
 #   conn = create_connection('cis3368.cygrl7flcnjt.us-east-2.rds.amazonaws.com', 'admin', 'Amaterasu24!', 'cis3368db')
 #   sql = "SELECT * FROM trip"
 #   trip = execute_read_query(conn, sql)
 #   results = []
#
 #  #append and return the results by destinationid and jsonify 
 #   for tripname in trip:
 #       if tripname['destinationid'] == destinationid:
 #           results.append(tripname)
 #   return results

@app.route('/trip', methods=['GET'])
def get_trip():
    conn = create_connection('cis3368.cygrl7flcnjt.us-east-2.rds.amazonaws.com', 'admin', 'Amaterasu24!', 'cis3368db')
    sql = "SELECT * FROM trip"
    trip = execute_read_query(conn, sql)
    return trip
#the GET method for the trip  table is now working and wil return all entries in the body section of postman when the endpoint is sent


@app.route('/trip', methods=['POST'])
def add_trip():
    request_data = request.get_json()
     #i had to modify the destinationid request so that it would take the info from the body section in postman and post it to the table
    strid = request_data['destinationid']     
    newdestinationid = str(strid)
    newtripname = request_data['tripname']
    newtransportation = request_data['transportation']
    #i used the reference below to get an idea on how to take a date input in the format yyyy-mm-dd and insert into the db table
    #https://www.codegrepper.com/code-examples/python/how+to+convert+string+into+date+in+python
    #i had to change the datetime variable into a str so that it would get inserted into the table for both startdate and enddate
    startdate = (request_data['startdate'])
    #date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)  
    newstartdate = str(datetime.strptime(startdate, '%m-%d-%Y').date())
    enddate = request_data['enddate']
    newenddate = str(datetime.strptime(enddate, '%m-%d-%Y').date())
    
    #connection to db and sql query to insert into table
    conn = create_connection('cis3368.cygrl7flcnjt.us-east-2.rds.amazonaws.com', 'admin', 'Amaterasu24!', 'cis3368db')
    sql = "INSERT INTO trip (destinationid, tripname, transportation, startdate, enddate) VALUES ('"+newdestinationid+"','"+newtripname+"','"+newtransportation+"','"+newstartdate+"','"+newenddate+"')"
    execute_query(conn, sql)
    return 'Trip added successfully'

#this method is gong to update an entry in the trip table by destinationid
@app.route('/trip', methods=['PUT'])
def update_trip():
    request_data = request.get_json()
    #to pick and choose which animal to update we are going to reference which one with its id
    strId = request_data['id']
    requestedId = str(strId) 
     #i had to modify the destinationid request so that it would take the info from the body section in postman and post it to the table
    strid2 = request_data['destinationid']     
    putdestinationid = str(strid2)
    puttripname = request_data['tripname']
    puttransportation = request_data['transportation']
    #i used the reference below to get an idea on how to take a date input in the format yyyy-mm-dd and insert into the db table
    #https://www.codegrepper.com/code-examples/python/how+to+convert+string+into+date+in+python
    #i had to change the datetime variable into a str so that it would get inserted into the table for both startdate and enddate
    startdate = (request_data['startdate'])
    #date format as yyyy-mm-dd(2022-03-04) or mm-dd-yyyy(03-04-2022)  
    putstartdate = str(datetime.strptime(startdate, '%m-%d-%Y').date())
    enddate = request_data['enddate']
    putenddate = str(datetime.strptime(enddate, '%m-%d-%Y').date())

    
    conn = create_connection('cis3368.cygrl7flcnjt.us-east-2.rds.amazonaws.com', 'admin', 'Amaterasu24!', 'cis3368db')
    cursor = conn.cursor()
    sql = "UPDATE trip SET destinationid = %s, tripname = %s, transportation = %s, startdate = %s, enddate = %s WHERE id = %s" 
    val = (putdestinationid, puttripname, puttransportation, putstartdate, putenddate, requestedId)
    cursor.execute(sql, val)
    conn.commit()
    return 'Trip updated successfully'
    #method is now working with json data in the body section of postman

#delete method for the trip table is now working with data from the body section in postman 
@app.route('/trip', methods=['DELETE'])
def delete_trip():
    request_data = request.get_json()
    strId = request_data['destinationid']
    requestedId = str(strId)
    
    conn = create_connection('cis3368.cygrl7flcnjt.us-east-2.rds.amazonaws.com', 'admin', 'Amaterasu24!', 'cis3368db')
    sql = "Delete from trip WHERE destinationid = ('"+requestedId+"')"
    execute_query(conn, sql)
    return 'Trip was deleted successfully'

#this endpoint is going to post information for your trip into the destination table by id
@app.route('/destination', methods=['POST']) #I got it to post to the zoo table
def post_destination():
    request_data = request.get_json() 
    strid = (request_data['id'])  
    tripid = str(strid)    
    tripcountry = request_data['country']
    tripcity = request_data['city']
    tripsights = request_data['sightseeing']

    #connection to the db
    conn = create_connection('cis3368.cygrl7flcnjt.us-east-2.rds.amazonaws.com', 'admin', 'Amaterasu24!', 'cis3368db')
    sql = "INSERT INTO destination (id, country, city, sightseeing) VALUES ('"+tripid+"','"+tripcountry+"','"+tripcity+"','"+tripsights+"')"
    execute_query(conn, sql)
    return 'Destination was added succesfully'

#post method is now working for the destination table

@app.route('/destination', methods=['GET'])
def get_destination():
    conn = create_connection('cis3368.cygrl7flcnjt.us-east-2.rds.amazonaws.com', 'admin', 'Amaterasu24!', 'cis3368db')
    sql = "SELECT * FROM destination"
    destination = execute_read_query(conn, sql)
    return destination
#the GET method for the destination table is now working and wil return all entries in the body section of postman when the endpoint is sent

app.run()