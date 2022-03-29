

import requests
import json,datetime,time
from flask import Flask,request,jsonify
import os
from pprint import pprint
import uuid
from pprint import PrettyPrinter
from dotenv import load_dotenv
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate  import Migrate


load_dotenv()  # take environment variables from .env.
pp = PrettyPrinter(indent=4)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://dcaruser:NVlMUDRKQk83VQ==@https://3.7.109.206:5432/dcardb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string'
db = SQLAlchemy(app)
# print(db,"DB ------------")
migrate = Migrate(app,db)

class CONFIG :
    apiBaseUrl = os.getenv("apiBaseUrl")
config = CONFIG()




class User(db.Model) :
    id = db.Column(db.Integer, primary_key=True)
    wso2UserId = db.Column(db.String(255), nullable=False)
    userName = db.Column(db.String(255), nullable=False)
    providerName = db.Column(db.String(255), nullable=False)
    apiKey = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phoneNumber = db.Column(db.String(255), nullable=False)

    def __init__(self,data) :
        self.wso2UserId = data["wso2UserId"]
        self.userName = data["userName"]
        self.providerName = data["providerName"]
        self.apiKey = data["apiKey"]
        self.active = data["active"]
        self.email = data["email"]
        self.phoneNumber = data["phoneNumber"]
        





def validateJSON(Data):
    is_valid = True
    for key in ["phoneNumber","email","userName","providerName"] :
        if(key not in Data) :
            is_valid = False
    try:
        json.dumps(Data)
    except ValueError as err:
        is_valid = False
    return is_valid

def update_db(data) :
    entry = User(data)
    db.session.add(entry)
    db.session.commit()
    


    





def get_dentity_service_body(email,phoneNumber,userName,providerName) :
    user_email = {}
    user_email["type"] = "home"
    user_email["value"] = email
    name = {}
    user_phone = {}
    user_phone["type"] = "work"
    user_phone["value"] = phoneNumber
    name["givenName"] = providerName
    name["familyName"] = ""
    user_role = {}
    user_role["type"]="default"
    user_role["value"] = "Internal/everyone,dcar:dcaralg1v1"
    identity_service_body_dict = {}
    identity_service_body_dict["emails"] = []
    identity_service_body_dict["phoneNumbers"] = []
    identity_service_body_dict["roles"] = []
    identity_service_body_dict["emails"].append(user_email)
    identity_service_body_dict["phoneNumbers"].append(user_phone)
    identity_service_body_dict["roles"].append(user_role)
    identity_service_body_dict["userName"] = userName
    identity_service_body_dict["active"] = True
    identity_service_body_dict["name"] = name
    return json.dumps(identity_service_body_dict)   
    
     
@app.route('/users',methods=["POST"])

def create_user():
    apiResponse = None
    body_data = request.get_json()
    phoneNumber = body_data["phoneNumber" ]
    email = body_data["email"]
    userName = body_data["userName"]
    providerName = body_data["providerName"]
    isValid = validateJSON(body_data)
    if(isValid == True) :
        identity_service_body = get_dentity_service_body(email,phoneNumber,userName,providerName) 
        response = requests.post(config.apiBaseUrl,data=identity_service_body,headers={"Content-Type": "application/json"},verify=False) 
        # response = {
        #         "id": "123456",
        #         "wso2UserId": "366e59e7-4df6-45b3-be9e-478ed31e4d10",
        #         "userName": "alg1v1",
        #         "providerName": "Apple",
        #         "active": 0,
        #         "email": "appleuser@apple.com",
        #         "phoneNumber": "+91-9865321770",
        # }
        if response.status_code == 200 :
        # if(True) :
             apiKey = uuid.uuid4().hex
             body_data["apiKey"] = apiKey
             wso2UserId = response.wso2UserId
            #  wso2UserId = response["wso2UserId"]

             body_data["wso2UserId"] = wso2UserId
             update_db(body_data)
             apiResponse = body_data

        # pp.pprint(identity_service_body)
        # return json.dumps(identity_service_body)
    else :
        apiResponse = "Invalid body content"

    return json.dumps(apiResponse)



# main driver function
if __name__ == '__main__':
	# run() method of Flask class runs the application
	# on the local development server.
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
    db.create_all()
