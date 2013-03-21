from flask import session, redirect, flash, request, url_for
from flask_oauth import OAuth

from deploystream import app
from deploystream.apps.oauth import get_oauth_token, set_oauth_token


oauth = OAuth()
github_oauth = oauth.remote_app('github',
    base_url='https://api.github.com/',
    request_token_url=None,
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    consumer_key=app.config['GITHUB_APP_ID'],
    consumer_secret=app.config['GITHUB_APP_SECRET'],
    request_token_params={
        'scope': 'user,repo'
    },
)

NAME = "github"


@github_oauth.tokengetter
def get_github_token(token=None):
    """Function used in the flask-oauth library to get a token.

    For now just get it from the session, or return ``None``.
    """
    return (get_oauth_token(session, NAME), '')


@app.route('/login')
def login():
    "Handler for calls to login via github."
    url = url_for('github_authorized',
                  next=request.args.get('next') or request.referrer or None,
                  _external=True)
    return github_oauth.authorize(callback=url)


@app.route('/oauth-authorized/')
@github_oauth.authorized_handler
def github_authorized(resp):
    "Call back for the github authorization."
    next_url = request.args.get('next') or url_for('homepage')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    set_oauth_token(session, NAME, resp['access_token'])

    user = github_oauth.get('/user')
    username = user.data['login']

    flash('You were signed in as {0}'.format(username))
    session['username'] = username
    return redirect(next_url)
