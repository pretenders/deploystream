from flask import session, redirect, flash, request, url_for
from flask_oauth import OAuth

from deploystream import app, db
from deploystream.apps.oauth import get_token, set_token
from deploystream.apps.users.models import User, OAuth as UserOAuth
from deploystream.apps.users.lib import (load_user_to_session,
        get_user_id_from_session)
from deploystream.providers.interfaces import class_implements, IOAuthProvider


def configure_oauth_routes(provider_classes):
    for name, cls in provider_classes.items():
        if class_implements(cls, IOAuthProvider):
            configure_route(cls.name, cls.get_oauth_data())

OAUTH_OBJECTS = {}


def configure_route(oauth_name, oauth_data):
    """
    Configure some app routes for the given oauth provider.

    The given oauth provider should have a key and secret in configuration at
    ``['oauth'][<oauth_name>]``.
    """
    key, secret = app.config['oauth'][oauth_name]

    oauth = OAuth().remote_app(
        oauth_name,
        consumer_key=key,
        consumer_secret=secret,
        **oauth_data
    )
    oauth.tokengetter_func = get_oauth_token(oauth_name)
    OAUTH_OBJECTS[oauth_name] = oauth
    args = (
        '/{0}-oauth-authorized/'.format(oauth_name),
        '{0}-oauth-authorized'.format(oauth_name),
        oauth.authorized_handler(oauth_authorized)
    )
    print("INFO: Configuring route: {0}".format(args))
    app.add_url_rule(
        *args
    )


def get_oauth_token(oauth_name):
    def func(token=None):
        """Function used in the flask-oauth library to get a token.

        For now just get it from the session, or return ``None``.
        """
        return (get_token(session, oauth_name), '')
    return func


def oauth_authorized(resp):
    "Call back for the oauth authorization."
    next_url = request.args.get('next') or url_for('homepage')
    oauth_name = request.args.get('oauth_name')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    set_token(session, oauth_name, resp['access_token'])

    # If registering, add a User and UserOAuth and load to session.
    # If Logging in, then just loading to session
    # If linking, then just adding a userOauth.

    current_user = get_user_id_from_session(session)
    remote_user = OAUTH_OBJECTS[oauth_name].get('/user')
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


@app.route('/oauth/<oauth_name>')
def link_up(oauth_name):
    "Handler for calls to login via github."
    return start_token_processing(oauth_name, islogin=True)


def start_token_processing(oauth_name, islogin=None):
    "Start processing oauth for the given name"
    url = url_for('{0}-oauth-authorized'.format(oauth_name),
                  next=request.args.get('next') or request.referrer or None,
                  oauth_name=oauth_name,
                  islogin=islogin,
                  _external=True)

    return OAUTH_OBJECTS[oauth_name].authorize(callback=url)
