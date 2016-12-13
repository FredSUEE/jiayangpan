import os

basedir = os.path.abspath(os.path.dirname(__file__))

# for testing oauth on http
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


APP_NAME = 'jiayangpan'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'cai-bu-dao-ba'

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# google auth2 info
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
GOOGLE_REDIRECT_URI = 'http://localhost:5000/oauth2callback'
GOOGLE_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
