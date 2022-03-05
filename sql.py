import mysql.connector
from mysql.connector import Error
from tabulate import tabulate
from flask import jsonify

#some functions that i plan to use during this project
#the connection code below is referenced from what we learned in 

def create_connection(host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name

            )
            print("Connection to MySQL DB successful")
        except Error as e:
            print(f"The error '{e}' occured.")
        return connection

#function that will be called in the main file to carry out the query in the app.route in which it is used in
def execute_query(connection, query):
    cursor = connection.cursor()
    try: 
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}'")

#i am planning to use this function with the app routes that pertain to the logs table
def execute_read_query(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return jsonify(result)
    except Error as e:
        print(f"The error '{e}' occured")