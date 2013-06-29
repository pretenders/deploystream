import flask.ext.restless
from flask import session
from flask.ext.restless import ProcessingException
from sqlalchemy.orm.exc import NoResultFound
from deploystream import app, db
from deploystream.apps.repo.models import Repo, user_repo_permissions

manager = flask.ext.restless.APIManager(app, flask_sqlalchemy_db=db)


def get_single_preprocessor(instance_id=None, **kw):
    try:
        user_id = session['user_id']
    except KeyError:
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)
    try:
        db.session.query(user_repo_permissions).filter(
            user_repo_permissions.c.user_id == user_id,
            user_repo_permissions.c.repo_id == instance_id).one()
    except NoResultFound:
        raise ProcessingException(message='Not Found',
                                  status_code=404)


def get_many_preprocessor(search_params=None, **kw):
    try:
        search_params['user_id'] = session['user_id']
    except KeyError:
        raise ProcessingException(message='Not Authorized',
                                  status_code=401)

# Create API endpoints, which will be available at /api/<tablename> by
# default. Allowed HTTP methods can be specified as well.
manager.create_api(Repo, methods=['GET'],
                   collection_name='repos',
                   preprocessors={
                      "GET_SINGLE": [get_single_preprocessor],
                      "GET_MANY": [get_many_preprocessor],
                   },
                   exclude_columns=Repo.EXCLUDE_AT_API,
                   )
