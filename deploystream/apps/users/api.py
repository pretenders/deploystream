from flask import session
from flask.ext.restless import APIManager, ProcessingException

from deploystream import app, db
from deploystream.apps.users.models import User

manager = APIManager(app, flask_sqlalchemy_db=db)


def deny(**kw):
    """Deny whatever calls this. Use as a pre or post processor."""
    raise ProcessingException(message='Not Authorized', status_code=401)


def check_auth(instance_id=None, **kw):
    "Check the current user has rights to get this user's details."
    # Here, get the current user from the session.
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])

    # Next, check if this is the current user:
    if not current_user.id == int(instance_id):
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(User, methods=['GET'],
                   collection_name='users',
                   preprocessors={
                      "GET_SINGLE": [check_auth],
                      "GET_MANY": [deny],
                   },
                   exclude_columns=User.EXCLUDE_AT_API,
                   )
