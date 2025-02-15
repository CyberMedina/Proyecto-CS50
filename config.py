from flask_session import Session
from flask_mysqldb import MySQL, MySQLdb
from dotenv import load_dotenv
import os
import mysql.connector


load_dotenv()

# Configuración de la base de datos

def connectionBD():
    db = mysql.connector.connect(
        host= os.getenv("DB_HOST"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        database = os.getenv("DB_NAME")
    )
    return db

# def connectionBD():
#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="1233456",
#         database="proyectocs50"
#     )
#     return db


