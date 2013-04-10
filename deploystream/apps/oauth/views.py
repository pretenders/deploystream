from flask import session, redirect, flash, request, url_for
from flask_oauth import OAuth

from deploystream import app
from deploystream.apps.oauth import get_token, set_token
from deploystream.providers.interfaces import class_implements, IOAuthProvider


def configure_oauth_routes(provider_classes):
    for name, cls in provider_classes.items():
        if class_implements(cls, IOAuthProvider):
            configure_route(cls.name, cls.get_oauth_data())

OAUTH_OBJECTS = {}


def configure_route(oauth_name, oauth_data):
    """
    Configure some app routes for the given oauth provider.

    It is assumed that config exists for::

        <oauth_name>_APP_ID
        <oauth_name>_APP_SECRET

    """
    key = app.config['{0}_APP_ID'.format(oauth_name)]
    secret = app.config['{0}_APP_SECRET'.format(oauth_name)]

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
    print "OAUTH AUTHORIZED", request.args
    next_url = request.args.get('next') or url_for('homepage')
    oauth_name = request.args.get('oauth_name')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    set_token(session, oauth_name, resp['access_token'])

    if request.args.get('islogin'):
        user = OAUTH_OBJECTS[oauth_name].get('/user')
        username = user.data['login']
        session['username'] = username

    return redirect(next_url)


@app.route('/login')
def login():
    "Handler for calls to login via github."
    return start_token_processing('github', islogin=True)


def start_token_processing(oauth_name, islogin=None):
    "Start processing oauth for the given name"
    url = url_for('{0}-oauth-authorized'.format(oauth_name),
                  next=request.args.get('next') or request.referrer or None,
                  oauth_name=oauth_name,
                  islogin=islogin,
                  _external=True)
    print "URL is ", url
    return OAUTH_OBJECTS[oauth_name].authorize(callback=url)
