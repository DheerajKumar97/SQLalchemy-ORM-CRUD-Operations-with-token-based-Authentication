from flask import Flask,request,jsonify,session,make_response
from DB_Connection import connection,host,user,password,database
from sqlalchemy import create_engine,MetaData,Table,Column,Integer,String,DateTime,Text,BLOB,Enum,update,text
from sqlalchemy.dialects.mysql.dml import Insert
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
import pandas as pd
import os
import string
import random
import json

app = Flask(__name__)
auth = HTTPBasicAuth()

env_path = 'config.env'
load_dotenv(dotenv_path=env_path)

token_size = os.environ.get("token_size")

class _customer_database_ :
    Meta = MetaData()
    UserSession1 = Table(
        'UserSession1', Meta,
        Column('UserID', Integer,primary_key=True), 
        Column('Token', String),
        Column('User_Agent', String),
    )

class _Customer_database_ :
    Meta = MetaData()
    User = Table(
        'User', Meta,
        Column('UserID', Integer,primary_key=True), 
        Column('Username', String),
        Column('Pass', String),
        Column('FirstName', String),
        Column('LastName', String),
    )


@auth.verify_password
def verify(username,passw):
	engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ.get("user"),os.environ.get("password"),os.environ.get("host"),os.environ.get("database")))
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	value = session.query(_Customer_database_.User).filter_by(Username=username,Pass=passw).first()[0]
	return value


@auth.login_required
def login_valdidate(username,pas):

	engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ.get("user"),os.environ.get("password"),os.environ.get("host"),os.environ.get("database")))
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	value = session.query(_Customer_database_.User).filter_by(Username=username,Pass=passw).first()[0]
	
	

def verify_token(token):

	engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ.get("user"),os.environ.get("password"),os.environ.get("host"),os.environ.get("database")))
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	value = session.query(_customer_database_.UserSession1).filter_by(Token=token).first()[1]
	if(value==token):
		return True
	else:
		return False



def insert_val(UserID,token_pass,User_Agent):

    engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ.get("user"),os.environ.get("password"),os.environ.get("host"),os.environ.get("database")))
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    conn = engine.connect()
    ins = Insert(_customer_database_.UserSession1).values(UserID=UserID,Token=token_pass,User_Agent=User_Agent)
    conn = engine.connect()
    result = conn.execute(ins,{'UserID':UserID,'Token':token_pass,'User_Agent':User_Agent})
	# con=connection
	# sql_q = "INSERT INTO UserSession1 (UserID,Token,User_Agent) VALUES (%(UserID)s,%(Token)s,%(User_Agent)s)"
	# connection.execute(sql_q,{'UserID':UserID,'Token':token_pass,'User_Agent':User_Agent})


@app.route('/login/',methods=['GET'])
@auth.login_required
def login_func():
	token = random_token()
	user_agent = request.headers.get('User-Agent')
	insert_val(auth.current_user(),token,user_agent)
	return json.dumps({'User_ID': auth.current_user(),'Your_Token' : token})


def random_token(size=int(token_size), chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
