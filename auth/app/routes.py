from app import app
from flask import request
import requests



@app.route('/authenticate', methods = ['GET'])
def authenticate():
    data = request.get_json()
    if 'uname' not in data or 'pwd' not in data:
        return 'bad request'
    username = data['uname']
    password = data['pwd']
    user = {'uname': username, 'pwd': password}
    headers = {'Content-Type': 'application/json'}
    try:
        data = requests.post('http://127.0.0.1:5001/login', json=user, headers=headers).json()
    except Exception as e:
        return 'NOK'
    if data['method'] == 1:
        data['method': 'external authentication process']
        return data
    
    return data
