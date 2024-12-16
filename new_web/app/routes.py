from app import app
from flask import render_template, flash, redirect, url_for
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
        
        user = User.do_auth(username, password)
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
    data = requests.get('http://127.0.0.1:5001/login').json()
    return render_template('events.html', title='Events', events=data)


