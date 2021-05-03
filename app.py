from flask import Flask,request,jsonify,session,make_response
from DB_Connection import connection,host,user,password,database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker
import sqlalchemy
from flask_cors import CORS
import api_connector
import json
import pandas as pd


app = Flask(__name__)
CORS(app)



class _customer_ :
    meta = MetaData()
    customer = Table(
       'customer', meta,
       Column('Customer_id', Integer, primary_key = True), 
       Column('Customer_name', String), 
       Column('Registration_date', String), 
       Column('Customer_Requirement', String),
    )

	
	
@app.route('/',methods=['GET'])
def Access_API():
	return {'Error':404 ,'Action' : 'Accessing API','Message':'Access your API with /login'}



@app.route('/login/',methods=['GET'])
def login_function():
	return api_connector.login_func()



@app.route('/customer/',methods=['GET'])
@app.errorhandler(502)
def customer():
    token=request.headers.get('token')
    if api_connector.verify_token(token):

        if request.method == 'GET':

            engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ.get("user"),os.environ.get("password"),os.environ.get("host"),os.environ.get("database")))
            s = select([_customer_.customer])
            result = engine.execute(s)
            cust=[]
            for i in result:
                cust.append(i)
            df = pd.DataFrame(cust,columns=['Customer_id','Customer_name','Registration_date','Customer_Requirement']).T.to_json()
            return {"Status":"Successful","Response":json.loads(df)}
        return {"Status":"Warning","Message":"API is not Properly executed"}
    else:
        return {"Status":"Failed","Error":502,"Message":"Invalid Token, direct access to api lead to potential security breach"}



@app.route('/customer/id/<string:id>/',methods=['GET'])
def id(id):
    token=request.headers.get('token')
    if api_connector.verify_token(token):

        engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ.get("user"),os.environ.get("password"),os.environ.get("host"),os.environ.get("database")))
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        res = session.execute(select([_customer_.customer]).where(_customer_.customer.c.Customer_id==id))
        record =[]
        for i in res:
            record.append(i)
        rec = pd.DataFrame(record,columns=['Customer_id','Customer_name','Registration_date','Customer_Requirement']).T.to_json()
        return {"Status":"Successful","Response":json.loads(rec)}
    else:
        return {"Status":"Failed","Error":502,"Message":"Invalid Token, direct access to api lead to potential security breach"}



@app.route('/customer/addcustomer/', methods=['GET', 'POST'])
def addcustomer():
    token=request.headers.get('token')
    if api_connector.verify_token(token):
        if request.method == 'POST':

            json_dict = request.get_json()
            cust_name = str(json_dict['cust_name'])
            reg_date = str(json_dict['reg_date'])
            cust_req = str(json_dict['cust_req'])
            ins = _customer_.customer.insert()
            ins = _customer_.customer.insert().values(Customer_name=cust_name, \
                                    Registration_date = reg_date,Customer_Requirement=cust_req)
            engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ.get("user"),os.environ.get("password"),os.environ.get("host"),os.environ.get("database")))
            conn = engine.connect()
            result = conn.execute(ins,{'Customer_name':cust_name, 'Registration_date':reg_date, 'Customer_Requirement':cust_req})
            return {"Status":"Successful","Message":"Successfully Written in Database"}
        return {"Status":"Warning","Message":"API is not Properly executed"}
    else:
        return {"Status":"Failed","Error":502,"Message":"Invalid Token, direct access to api lead to potential security breach"}




@app.route('/customer/deletecustomer/', methods=['GET', 'POST'])
def deletecustomer():
    token=request.headers.get('token')
    if api_connector.verify_token(token):
        if request.method == 'POST':

            json_dict = request.get_json()
            cust_id = str(json_dict['cust_id'])
            engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(os.environ.get("user"),os.environ.get("password"),os.environ.get("host"),os.environ.get("database")))
            conn = engine.connect()
            stmt = _customer_.customer.delete().where(_customer_.customer.c.Customer_id == cust_id)
            conn.execute(stmt,{'Customer_id':cust_id})
            return {"Status":"Successful","Message":"Successfully Deleted from Database"}
        return {"Status":"Warning","Message":"API is not Properly executed"}
    else:
        return {"Status":"Failed","Error":502,"Message":"Invalid Token, direct access to api lead to potential security breach"}



@app.route('/customer/updatecustomer/', methods=['GET', 'POST'])
def updatecustomer():
    
    token=request.headers.get('token')
    if api_connector.verify_token(token):
        if request.method == 'POST':

            json_dict = request.get_json()
            cust_id = str(json_dict['cust_id'])
            cust_name = str(json_dict['cust_name'])
            reg_date = str(json_dict['reg_date'])
            cust_req = str(json_dict['cust_req'])
            conn = engine.connect()
            stmt=_customer_.customer.update().where(\
                    _customer_.customer.c.Customer_id==cust_id).values(Customer_name=cust_name,\
                    Registration_date=reg_date,\
                    Customer_Requirement=cust_req)
            conn.execute(stmt)
            return {"Status":"Successful","Message":"Successfully Updated in Database"}
        return {"Status":"Warning","Message":"API is not Properly executed"}
    else:
        return {"Status":"Failed","Error":502,"Message":"Invalid Token, direct access to api lead to potential security breach"}



if __name__ == '__main__':
    app.run(port=5500,debug=True)
