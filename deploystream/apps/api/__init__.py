import flask.ext.restless
from flask import session
from flask.ext.restless import ProcessingException

from deploystream import app, db
from deploystream.apps.users.models import User

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)


def check_auth(instance_id=None, **kw):
    # Here, get the current user from the session.
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])

    print current_user.id, instance_id
    # Next, check if this is the current user:
    if not current_user.id == int(instance_id):
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(User, methods=['GET'],
                   preprocessors=dict(GET_SINGLE=[check_auth]))

# TODO:
# Write tests for:
# - Can't grab a list of users.
# - Can't grab a user that isn't you.
# - Grabbing /profile (or similar) returns you.
#
# Change the angular Users stuff to:
# - Call /profile to get you
# - Call /oauth/ to get a list of possible oauths
# - Fillin the details using the oauth_keys returned in /profile.
