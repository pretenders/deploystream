from deploystream import db
from deploystream.apps.users import constants as USER


class User(db.Model):

    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(20))
    role = db.Column(db.SmallInteger, default=USER.USER)
    status = db.Column(db.SmallInteger, default=USER.NEW)
    oauth_keys = db.relationship('OAuth', backref='user')

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password

    def getStatus(self):
        return USER.STATUS[self.status]

    def getRole(self):
        return USER.ROLE[self.role]

    def __repr__(self):
        return '<User %r>' % (self.name)


class OAuth(db.Model):

    __tablename__ = 'users_oauth'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
    service = db.Column(db.String(20))
    service_user_id = db.Column(db.String(120))

    db.UniqueConstraint('service', 'service_user_id', name='service_user')
