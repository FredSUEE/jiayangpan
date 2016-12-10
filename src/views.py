from flask import (
    render_template,
    redirect,
    url_for,
    session,
    request
)
from flask_login import (
    current_user,
    login_user
)
from requests_oauthlib import OAuth2Session

from src import app, db, login_manager
from .models import User

import json
import urllib2


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@app.route('/index')
def index():
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           posts=posts)


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        app.config['GOOGLE_AUTH_URI'],
        access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)

# http://localhost:5000/oauth2callback?state=NguTIuLLjUZkW9W6kd4LonYnXSzxRL&code=4/jp91T4AsyxoYuwa2pyBd7yyJtwISyXWw7OzqiwbIr2Q#


@app.route('/oauth2callback')
def callback():
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=session['oauth_state'])
        try:
            token = google.fetch_token(
                app.config['GOOGLE_TOKEN_URI'],
                client_secret=app.config['GOOGLE_CLIENT_SECRET'],
                authorization_response=request.url)
        except urllib2.HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        resp = google.get(app.config['GOOGLE_USER_INFO'])
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User()
                user.email = email
            user.name = user_data['name']
            print(token)
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'


def get_google_auth(state=None, token=None):
    if token:
        return OAuth2Session(
            app.config['GOOGLE_CLIENT_ID'],
            token=token)
    if state:
        return OAuth2Session(
            app.config['GOOGLE_CLIENT_ID'],
            state=state,
            redirect_uri=app.config['GOOGLE_REDIRECT_URI'])
    oauth = OAuth2Session(
        app.config['GOOGLE_CLIENT_ID'],
        redirect_uri=app.config['GOOGLE_REDIRECT_URI'],
        scope=app.config['GOOGLE_AUTH_SCOPE'])
    return oauth
