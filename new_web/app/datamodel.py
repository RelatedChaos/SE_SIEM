from flask_login import UserMixin
import requests
from app import login

class User(UserMixin):
    def __init__(self, username, user_id, role):
        self.username = username
        self.id = user_id
        self.role = role


    @staticmethod
    def do_auth(username, password):

        user = {'uname': username, 'pwd': password}
        headers = {'Content-Type': 'application/json'}
        data = requests.post('http://127.0.0.1:5001/login', json=user, headers=headers)

        if data.status_code == 200:
            user_id = data.json().get("user_id")
            role = data.json().get("role")
            return User(user_id, username, role)
        return None
    
@login.user_loader
def load_user(id):
    return User(id, "Unknown", "Unknown")