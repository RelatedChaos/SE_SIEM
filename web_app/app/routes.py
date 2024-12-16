from app import app
from app import db
from app.models import User
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa



@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():

        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))

        if user is None:
            flash('Please enter credentials')
            return redirect(url_for('login'))
        
        if user.connection_method == 0 and not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        if user.connection_method == 1:
            flash('LDAP authentication not configured')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))