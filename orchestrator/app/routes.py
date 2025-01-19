from app import app
from flask import request
import requests
from subprocess import run
import os


@app.route('/do_execute', methods = ['GET'])
def execute():
    print('execute do exec')
    data = request.get_json()
    print(data)
    resp = run(["python", f"orchestrator/store/{data['location']}.py"], capture_output=True, text=True)
    print(resp.stdout)
    return {'response': resp.stdout}

@app.route('/orchestration', methods = ['POST', 'PUT'])
def edit_orchestration():
    data = request.get_json()
    if request.method == 'POST':
        return {'status': '200', 'message': 'edited orchestration'}
    elif request.method == 'PUT':
        return {'status': '200', 'message': 'created orchestration'}
