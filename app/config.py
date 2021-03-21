import os
from dotenv import load_dotenv, find_dotenv

#basedir = os.path.abspath(os.path.dirname(__file__))
#load_dotenv(os.path.join(basedir, '.env'))
load_dotenv(find_dotenv())

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../content.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_FOLDER = 'app/static/files'
    
