import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Event': Event}


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)