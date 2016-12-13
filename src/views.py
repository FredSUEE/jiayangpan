from flask import (
    render_template,
    redirect,
    url_for,
    session,
    request,
    g,
    flash
)
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required
)

from src import app, db, login_manager
from models.user import User
from util.authenticate import get_google_auth

import json
import urllib2


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/profile')
@login_required
def profile():
    user = g.user
    # unicode user_id
    user_id = request.args.get('id')

    # need to query for the user object for other users' pages
    if user_id is not None and user.id != int(user_id):
        user = User.query.filter_by(id=user_id).first()
    return render_template('profile.html',
                           user=user)


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
            # print(token)
            # TODO: no need to add user if already in the DB
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        return 'Could not fetch your information.'


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', status_code=404), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', status_code=500), 500
