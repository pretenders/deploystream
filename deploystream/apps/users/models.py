from datetime import datetime

from werkzeug import generate_password_hash

from deploystream import db
from deploystream.apps.base.models import Base

from . import constants as USER_CONSTANTS


class User(Base, db.Model):

    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(20))
    role = db.Column(db.SmallInteger, default=USER_CONSTANTS.USER)
    status = db.Column(db.SmallInteger, default=USER_CONSTANTS.NEW)
    created = db.Column(db.DateTime, default=datetime.now)

    oauth_keys = db.relationship('OAuth', backref='user')
    repos = db.relationship('Repo', backref='user')

    EXCLUDE_AT_API = ['password', 'role', 'status']

    @classmethod
    def create_user(cls, username, email, password):
        user = cls(username, email, generate_password_hash(password))
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()
        return user

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def getStatus(self):
        return USER_CONSTANTS.STATUS[self.status]

    def getRole(self):
        return USER_CONSTANTS.ROLE[self.role]

    def __repr__(self):
        return '<User %r>' % (self.username)


class OAuth(Base, db.Model):

    __tablename__ = 'users_oauth'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    service = db.Column(db.String(20))
    service_user_id = db.Column(db.String(120))
    service_username = db.Column(db.String(50))

    # A user on an external service should only exist once in deploystream.
    db.UniqueConstraint('service', 'service_user_id', name='service_user')

    # Each user in deploystream should only have each service oauth'd once.
    db.UniqueConstraint('user_id', 'service', name='user_service')
