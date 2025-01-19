from app import app
from app import db
from app.models import User, Event, AutomaticResponse, Configuration, Incident
import sqlalchemy as sa
from flask import request
from flask_httpauth import HTTPBasicAuth
from datetime import datetime, timezone

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
          'role': user.role,
          'method': user.connection_method
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
     
@app.route('/orchestration', methods = ['GET'])
def get_orchestration():
     ret = AutomaticResponse.query.all()
     resp = [orc.to_dict() for orc in ret]
     return resp

@app.route('/orchestration', methods = ['PUT'])
def put_orchestration():
     data = request.get_json()
     orchestration = AutomaticResponse()
     orchestration.action_details = data['details']
     orchestration.action_type = data['type']
     orchestration.script_location = data['name']
     orchestration.status = data['status']
     db.session.add(orchestration)
     db.session.commit()
     return '200'


@app.route('/configuration', methods = ['GET', 'POST'])
def configurations():
     data = request.get_json()
     print(request.headers, request.data)
     if request.method == 'GET':
          if 'type' in data:
               configuration = Configuration.query.filter_by(config_type = data['type']).all()
               configurations = [conf.to_dict() for conf in configuration]
               return configurations
          else:
               configuration = Configuration.query.all()
               configurations = [conf.to_dict() for conf in configuration]
               return configurations
     elif request.method == 'POST':
          configuration = Configuration()
          configuration.config_name = data['name']
          configuration.config_type = data['type']
          configuration.value = data['value']
          db.session.add(configuration)
          db.session.commit()
          return '200'
     
@app.route('/incident', methods = ['GET','PUT'])
def incidnet():
     data = request.get_json()
     if request.method == 'GET':
          if 'id' in data:
               incident = Incident.query.filter_by(id = data['id']).all()
               ret = [inc.to_dict() for inc in incident]
               return ret
          else:
               incident = Incident.query.all()
               ret = [inc.to_dict() for inc in incident]
               return ret
     elif request.method == 'PUT':
          new_incident = Incident(
               incident_timestamp=datetime.now(timezone.utc),
               status=data["status"],
               description=data["description"],
               notes=data.get("notes"),  # Optional field
               event_id=data["event_id"],
               user_id=data["user_id"],
               correlation_id=data["correlation_id"],
          )
          db.session.add(new_incident)
          db.session.commit()
          return '200'
          

@app.route('/incident/<int:incident_id>', methods=['POST'])
def edit_incident(incident_id):
     data = request.get_json()
     incident = Incident.query.get_or_404(incident_id, description=f"Incident with ID {incident_id} not found.")
     if "status" in data:
          incident.status = data["status"]
     if "description" in data:
          incident.description = data["description"]
     if "notes" in data:
          incident.notes = data["notes"]
     if "event_id" in data:
          incident.event_id = data["event_id"]
     if "user_id" in data:
          incident.user_id = data["user_id"]
     if "correlation_id" in data:
          incident.correlation_id = data["correlation_id"]
     incident.updated_at = datetime.now(timezone.utc)
     db.session.commit()
     