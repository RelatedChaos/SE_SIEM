from app import app
from flask import request
import requests



@app.route('/config', methods = ['GET', 'POST'])
def exec_config():
    print('execute config')
    data = request.get_json()
    print(request.headers)
    print(request.data)
    if request.method == 'POST':
        return {'response': 'changed config'}
    elif request.method == 'GET':
        configurations = {
            "server_timeout": "30",
            "max_connections": "100",
            "enable_logging": "True",
            "log_level": "INFO"
        }
        headers = {'Content-Type': 'application/json'}
        confs = requests.get('http://127.0.0.1:5001/configuration', headers=headers, json={}).json()
        return {'response': confs}
