from flask import session, redirect, flash, request, url_for
from flask_oauth import OAuth

from deploystream import app, db
from deploystream.apps.oauth import get_token, set_token
from deploystream.apps.users.models import User, OAuth as UserOAuth
from deploystream.apps.users.lib import (load_user_to_session,
        get_user_id_from_session)
from deploystream.lib.transforms import as_json
from deploystream.providers.interfaces import class_implements, IOAuthProvider

from . import constants as OAUTH_CONSTANTS


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

    current_user_id = get_user_id_from_session(session)
    remote_user = OAUTH_OBJECTS[oauth_name].get('/user')
    remote_user_id = remote_user.data['id']

    user = get_or_create_user_oauth(
        current_user_id, remote_user_id, oauth_name, remote_user.data['login']
    )

    load_user_to_session(session, user)

    return redirect(next_url)


def get_or_create_user_oauth(user_id, service_user_id, service_name,
                             service_username):
    """
    Get or create OAuth information and Users with the given information.

    Handles a number of scenarios:
        - No user id is known. (ie user is logged out)
            - OAuth object exists: return the associated user.
            - OAuth object doesn't exist: create it, along with a user and link
              them
        - User id is known (ie user is logged in)
            - Create and link the OAuth data to the account.

    :param user_id:
        The id of the currently logged in user. Or ``None`` if logged out.
    :param service_user_id:
        The id of the user according to the external service.
    :param service_name:
        The name used internally to reference the external service.
    :param service_username:
        The username that the service knows this user by. This will be used to
        create the account in deploystream if logging in for the first time.
    """
    if not user_id:
        # We're either logging in or registering
        oauth_obj = UserOAuth.query.filter_by(service_user_id=service_user_id,
                                              service=service_name).first()
        if not oauth_obj:
            # Create a user and an OAuth linked to it.
            current_user = User(username=service_username)
            oauth = UserOAuth(service_user_id=service_user_id,
                              service=service_name,
                              service_username=service_username)
            oauth.user = current_user
            db.session.add(current_user)
            db.session.add(oauth)
            db.session.commit()
            user_id = current_user.id
            user = current_user
        else:
            user_id = oauth_obj.user.id
            user = oauth_obj.user

    else:
        # We're linking the account
        oauth = UserOAuth(service_user_id=service_user_id,
                          service=service_name,
                          service_username=service_username,
                          user_id=user_id)
        db.session.add(oauth)
        db.session.commit()
        user = oauth.user

    return user


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


@app.route('/oauth/')
@as_json
def list():
    """Returns the list of supported Oauths

    This may want to end up in the database and be turned into a /api/ url.
    """
    return OAUTH_CONSTANTS.OAUTHS
