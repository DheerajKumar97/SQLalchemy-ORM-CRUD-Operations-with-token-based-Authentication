from flask import Flask,request,jsonify,session,make_response
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


env_path = 'config.env'
load_dotenv(dotenv_path=env_path)


host = os.environ.get("host")
user = os.environ.get("user")
password = os.environ.get("password")
database = os.environ.get("database")


app = Flask(__name__)

def Database_connection(dbuser, dbpass, dbhost, dbname):
    try:
        engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(dbuser,dbpass,dbhost,dbname))
        connection = engine.connect()
        print(" MySQL DB Connected successfully")
    except:
        print("The error occurred in DB Connection")
    return connection


connection = Database_connection(user,password,host,database)
