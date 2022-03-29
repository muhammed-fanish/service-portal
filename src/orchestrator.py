
import requests
import json,datetime,time
from flask import Flask,request,jsonify
import os
from pprint import pprint
app = Flask(__name__)




@app.route('/data-processor',methods=["POST"])
def execute_data_processor():
    body_data = request.get_json()
    callback_url = body_data['metadata']['call_back_url']
    input = body_data['input']
   
    # time.sleep(60)
   
    res = {}
    res['metadata'] = {"taskname":body_data['metadata']['taskname']}
    res['output'] = "Canser detected"
    response = requests.post(callback_url,data=json.dumps(res),headers={"Content-Type": "application/json"},verify=False) 
    return json.dumps(res)

    
@app.route('/provider',methods=["POST"])
def execute_provider():
    response = requests.post("http://10.62.26.21:5015/orchestrator-service",data=json.dumps({"attr1":"val1","attr2" :"val2"}),headers={"Content-Type": "application/json"},verify=False) 
    if (response.status_code == 201) :
        # time.sleep(120)
        res = requests.get(response.callback_url)
        return json.dumps(res)
    return json.dumps(response)


@app.route('/orchestrator-service',methods=["POST"])
def orchestrator_service():
     body_data = request.get_json()
     print(body_data,"BODY DATA")
     orch_out ={}
     orch_out["status_code"]=201
     orch_out["callback_url"]="https://jsonplaceholder.typicode.com/posts"
     return(json.dumps(orch_out))


@app.route('/',methods=["GET"])
def hai():
     return(json.dumps("HAI"))










if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5015"), debug=True)



