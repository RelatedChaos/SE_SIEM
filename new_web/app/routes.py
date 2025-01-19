from app import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required
from app.forms import LoginForm
import requests
from app.datamodel import User

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
    return render_template('login.html', title='Sign In', form=form)


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
    data = {}
    data = requests.get('http://127.0.0.1:5001/events', json={'page': '1', 'per_page': '100'}).json()
    return render_template('events.html', title='Events', events=data['events'])

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

