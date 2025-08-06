import mysql.connector

def get_connection():
    return  mysql.connector.connect(
    host="aws.connect.psdb.cloud",
    user="abcd123",
    password="Xyz@123",
    database="my_flutter_login",
    port=3306
)
