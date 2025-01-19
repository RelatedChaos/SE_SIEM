from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required
from app.forms import LoginForm
import requests
from app.datamodel import User
import json

@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        print(username, password)
        if username is None:
            flash('Please enter credentials')
            return redirect(url_for('login'))
        
        try:
            user = User.do_auth(username, password)
        except Exception as e:
            flash('Invalid login')
            return redirect(url_for('login'))
        if user:
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('invalid credentials')
    return render_template('login.html', title='Sign In', form=form, hide_header=True)


@app.route('/debug_db')
def debug():
    data = {}
    user = {'uname': 'sysadmin', 'pwd': 'sysadmin'}
    headers = {'Content-Type': 'application/json'}
    data = requests.post('http://127.0.0.1:5001/login', json=user, headers=headers).json()
    
    return render_template('debug_db.html', title='Debug', db=data)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/events')
def get_events():
    filter_text = request.args.get('filter', '')
    page = request.args.get('page', '1')
    per_page = request.args.get('per_page', '100')

    # Fetch data from the external service
    response = requests.get('http://127.0.0.1:5001/events', json={
        'page': page,
        'per_page': per_page
    })
    data = response.json()

    return render_template(
        'events.html',
        title='Events',
        events=data['events'],
        filter_text=filter_text,
        page=int(page),
        per_page=int(per_page),
        total_pages=data.get('total_pages', 1)  # Assume the API provides total pages
    )

@app.route('/orchestration')
def get_orchestration():
    data = {}
    data = requests.get('http://127.0.0.1:5001/orchestration').json()
    return render_template('orchestration.html', title='Orchestration', orchestrations = data)

@app.route('/process_orc')
def process_orc():
    print('exec proc')
    orc = request.args.get('orc')
    headers = {'Content-Type': 'application/json'}
    resp = requests.get('http://127.0.0.1:5006/do_execute', headers=headers, json={'location':orc}).json()
    print(resp)
    return jsonify({"message": f"Orchestration {orc} processed successfully response is {resp['response']}!"})

@app.route('/create_orchestration')
def create_orchestration_page():
    return render_template('create_orchestration.html')

@app.route('/save_orchestration', methods=['POST'])
def save_orchestration():
    # Retrieve form data
    name = request.form.get('name')
    code = request.form.get('code')
    orc_type = request.form.get('type')

    # Save orchestration logic here (e.g., save to a database or file)
    print(f"Name: {name}, Type: {orc_type}, Code: {code[:50]}...")

    # Redirect back to the orchestration page
    return redirect(url_for('orchestration_page'))

@app.route('/incidents')
def create_incidents_page():
    incidents = [
        {"id": 1, "title": "Brute force attack", "description": "Main server is not responding", "status": "Open", "created_at": "2025-01-01"},
        {"id": 2, "title": "Database Issue", "description": "Unable to connect to DB", "status": "In Progress", "created_at": "2025-01-15"},
        {"id": 3, "title": "Resolved Bug", "description": "Fixed critical bug in system", "status": "Closed", "created_at": "2025-01-10"}
    ]
    return render_template('incidents.html', incidents=incidents)

@app.route('/configuration', methods=['GET', 'POST'])
def create_config_page():
    headers = {'Content-Type': 'application/json'}
    conf = requests.get('http://127.0.0.1:5007/config', headers=headers, json={'data':'data'}).json()
    conf_items = conf['response']
    if request.method == 'POST':
        config_key = request.form.get('config_key')
        config_value = request.form.get('config_value')
        conf[config_key] = config_value
        return redirect(url_for('create_config_page'))
    return render_template('configuration.html', configurations=conf_items)
