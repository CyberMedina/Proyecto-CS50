from flask_session import Session
from flask_mysqldb import MySQL, MySQLdb
import mysql.connector


def connectionBD():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1233456",
        database="proyectocs50"
    )
    return db

