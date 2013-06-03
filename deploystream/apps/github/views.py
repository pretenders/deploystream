from flask import session, redirect, flash, request, url_for
from flask_oauth import OAuth

from deploystream import app, db
from deploystream.apps.oauth import get_token, set_token
from deploystream.apps.users.models import User, OAuth as UserOAuth
from deploystream.apps.users.lib import (load_user_to_session,
    get_user_id_from_session)

# TODO:
# Fix broken tests
# Add tests for Registering an account
# Add test for linking an account to github.
# Refactor oauth_authorized so that there are fewer paths.
# Move github into a sub url (/github/)

consumer_key, consumer_secret = app.config['oauth']['github']

OAUTH_DATA = {
    'base_url': 'https://api.github.com/',
    'request_token_url': None,
    'access_token_url': 'https://github.com/login/oauth/access_token',
    'authorize_url': 'https://github.com/login/oauth/authorize',
    'request_token_params': {
        'scope': 'repo'
    },
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
}
GITHUB_APP = OAuth().remote_app('github', **OAUTH_DATA)


@GITHUB_APP.tokengetter
def get_github_token():
    return get_token(session, 'github'), ''


@app.route('/github-oauth-authorized/', endpoint='github-oauth-authorized')
@GITHUB_APP.authorized_handler
def oauth_authorized(resp):
    "Call back for the oauth authorization."
    next_url = request.args.get('next') or url_for('homepage')
    oauth_name = 'github'
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    set_token(session, oauth_name, resp['access_token'])

    # If registering, add a User and UserOAuth and load to session.
    # If Logging in, then just loading to session
    # If linking, then just adding a userOauth.

    current_user = get_user_id_from_session(session)
    remote_user = GITHUB_APP.get('/user')
    remote_user_id = remote_user.data['id']

    if not current_user:
        # We're either logging in or registering
        oauth_obj = UserOAuth.query.filter_by(service_user_id=remote_user_id,
                                              service=oauth_name).first()
        if not oauth_obj:
            # Create a user and an OAuth linked to it.
            user = User(username=remote_user.data['login'])
            oauth = UserOAuth(service_user_id=remote_user_id,
                              service=oauth_name,
                              service_username=remote_user.data['login'])
            oauth.user = user
            db.session.add(user)
            db.session.add(oauth)
            db.session.commit()
        else:
            user = oauth_obj.user

        load_user_to_session(session, user)
    else:
        # We're linking the account
        oauth = UserOAuth(service_user_id=remote_user_id,
                          service=oauth_name,
                          service_username=remote_user.data['login'],
                          user_id=current_user)
        db.session.add(oauth)
        db.session.commit()

    return redirect(next_url)


@app.route('/github-register')
def login():
    "Handler for calls to login via github."
    from deploystream.apps.github import GithubProvider
    return GithubProvider.start_token_processing()
