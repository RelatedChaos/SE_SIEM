from app import app
from app import db
from app.models import User, Event
import sqlalchemy as sa
from flask import request
from flask_httpauth import HTTPBasicAuth

basic_auth = HTTPBasicAuth()

@basic_auth.verify_password
def verify_password(username, password):
    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user and user.check_password(password) and user.role == 'sysadmin':
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    return f'{status}'



@app.route('/')
@app.route('/index')
def index():
    return "App_DB_rests-here"

@app.route('/login', methods = ['POST'])
def login():
     data = request.get_json()
     if 'uname' not in data or 'pwd' not in data:
          return 'bad request'
     username = data['uname']
     password = data['pwd']
     user = db.session.scalar(sa.select(User).where(User.username == username))

     if user is None:
               return 'False'

     if user.connection_method == 0 and not user.check_password(password):
          return 'Login Failed'

     user_data = {
          'user_id': user.id,
          'username': user.username,
          'role': user.role
     }

     return user_data

@app.route('/users', methods = ['GET'])
def get_users():
     user_data = db.get_or_404(User, 1).to_dict()
     return user_data

@app.route('/users/create', methods = ['POST'])
@basic_auth.login_required
def create_user():

     data = request.get_json()

     if 'uname' not in data or 'pwd' not in data: 
          return 'must include username and password fields'
     if db.session.scalar(sa.select(User).where(User.username == data['uname'])):
          return 'please use a different username'
     
     user = User(username = data['uname'])
     user.set_password(data['pwd'])

     if 'role' in data:
          user.role = data['role']
     else:
          user.role = 'Analyst'

     if 'connection_method' in data:
          user.connection_method = data['connection_method']
     else:
          user.connection_method = 0
     

     db.session.add(user)
     db.session.commit()

     user_data = {
          'user_id': user.id,
          'username': user.username,
          'role': user.role
          }
     return user_data

@app.route('/events', methods = ['GET'])
def get_events():
     data = request.get_json()
     events = ''
     query = sa.select(Event).order_by(Event.p_datetime_timestamp.desc())
     ret = {'events': []}
     if 'page' in data:
          events = db.paginate(query, page=int(data['page']), per_page=int(data['per_page']), error_out=False).items
     else:
          events = db.paginate(query, page=1, per_page=50, error_out=False).items
     for event in events:
          ret['events'].append(event.to_dict())

     return ret

@app.route('/events', methods = ['POST'])
def post_events():
     data = request.get_json()
     if 'event' in data:
          ev = Event(raw_event=data['event'])
          db.session.add(ev)
          db.session.commit()
          return '200'
     
@app.route('/events/parse', methods = ['POST'])
def parse_events():
     data = request.get_json()
     if 'event' in data:
          ev = Event(raw_event=data['event'])
          ev.parse_raw()
          db.session.add(ev)
          db.session.commit()
          return '200'


