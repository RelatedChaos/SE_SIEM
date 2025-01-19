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
