from datetime import datetime

from deploystream import db
from deploystream.apps.users import constants as USER


class User(db.Model):

    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(20))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    created = db.Column(db.DateTime, default=datetime.now)

    oauth_keys = db.relationship('OAuth', backref='user')

    def __init__(self, username=None, email=None, password=None):
        self.username = username
        self.email = email
        self.password = password

    def getStatus(self):
        return USER.STATUS[self.status]

    def getRole(self):
        return USER.ROLE[self.role]

    def __repr__(self):
        return '<User %r>' % (self.username)


class OAuth(db.Model):

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

