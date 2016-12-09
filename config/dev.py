import os

basedir = os.path.abspath(os.path.dirname(__file__))


APP_NAME = 'jiayangpan'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'cai-bu-dao-ba'

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# google auth2 info
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = ''
AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
