from flask import session
from flask.ext.restless import APIManager, ProcessingException
from sqlalchemy.orm.exc import NoResultFound
from deploystream import app, db
from deploystream.apps.repo.models import Repo
from deploystream.apps.users.models import User

manager = APIManager(app, flask_sqlalchemy_db=db)


class Unauthorized(ProcessingException):
    def __init__(self):
        ProcessingException.__init__(self,
                                     message='Not Authorized',
                                     status_code=401)


def get_single_preprocessor(instance_id=None, **kw):
    """
    Preprocessor for getting a single repo. Handles permissions.

    401: If the user isn't logged in.
    404: If the repo ``instance_id`` does not exist.
    404: If the user logged in doesn't have rights to the repo.)
    """
    try:
        user_id = session['user_id']
    except KeyError:
        raise Unauthorized()
    try:
        Repo.query.filter_by(user_id=user_id).one()
    except NoResultFound:
        raise ProcessingException(message='Not Found',
                                  status_code=404)


def get_many_preprocessor(search_params=None, **kw):
    """
    Preprocessor for getting multiple repos. Handles permissions.

    Responsible for adding the search filters to ensure that the response only
    brings back repos relevant for this user. Not ALL repos.

    401: If the user isn't logged in.
    """
    try:
        if 'filters' not in search_params:
            search_params['filters'] = []

        # Filter on user id. Strange syntax, but this is what Restless is
        # after. HINT: if user-repos becomes many to many, change op to 'any'
        # and change ``name='user_id'`` to ``name='user__id'``.
        filt = dict(name='user_id', op='eq', val=session['user_id'])
        search_params['filters'].append(filt)
    except KeyError:
        raise Unauthorized()


def post_preprocessor(data, **kwargs):
    try:
        auth_user_id = session['user_id']
    except KeyError:
        raise Unauthorized()

    data['user_id'] = auth_user_id


# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Repo, methods=['GET', 'POST'],
                   collection_name='repos',
                   preprocessors={
                      "GET_SINGLE": [get_single_preprocessor],
                      "GET_MANY": [get_many_preprocessor],
                      "POST": [post_preprocessor]
                   },
                   exclude_columns=Repo.EXCLUDE_AT_API,
                   )
