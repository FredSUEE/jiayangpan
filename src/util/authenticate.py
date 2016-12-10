from requests_oauthlib import OAuth2Session
from src import app


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
