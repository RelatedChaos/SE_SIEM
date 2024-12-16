import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    Config_val = 'None'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'extremely_secret_key'
    EXTERNAL_SYSTEM_URL = 'http://127.0.0.1:5001'