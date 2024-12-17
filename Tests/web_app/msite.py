from app import app
import socket, select, queue
from socket import *
from app.models import Event
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import create_app, db
from app.models import User, Event, Task

from flask import Flask
from celery import Celery

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Task': Task}
