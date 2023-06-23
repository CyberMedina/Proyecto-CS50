from flask_session import Session
from flask_mysqldb import MySQL, MySQLdb
import mysql.connector


def connectionBD():
    db = mysql.connector.connect(
        host="proyectocs50.mysql.database.azure.com",
        user="localhost",
        password="cjs-1234",
        database="proyectocs50"
    )
    return db


