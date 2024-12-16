from app import app, db
from werkzeug.http import HTTP_STATUS_CODES

@app.errorhandler(404)
def not_found_error(error):
    return 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return 500

def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message