from os.path import join, dirname, abspath
from flask import session, redirect, flash, request, url_for
from flask_oauth import OAuth

from deploystream import app


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


@github_oauth.tokengetter
def get_github_token(token=None):
    """Function used in the flask-oauth library to get a token.

    For now just get it from the session, or return ``None``.
    """
    return session.get('github_token')


@app.route('/login')
def login():
    #why_oh_why()
    "Handler for calls to login via github."
    url = url_for('github_authorized',
                  next=request.args.get('next') or request.referrer or None,
                  _external=True)
    return github_oauth.authorize(callback=url)


@app.route('/oauth-authorized/')
@github_oauth.authorized_handler
def github_authorized(resp):
    "Call back for the github authorization."
    if resp is None:
        return 'Access denied: error=%s' % (request.args['error'])
    session['github_token'] = (resp['access_token'], '')
    user = github_oauth.get('/user')
    return 'Logged in as id=%s login=%s redirect=%s' % \
        (user.data['id'], user.data['login'], request.args.get('next'))
