from deploystream import db
from deploystream.apps.base.models import Base


class Repo(db.Model, Base):

    EXCLUDE_AT_API = ['users']

    __tablename__ = 'repo_repo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(200))

    user_id = db.Column(db.Integer, db.ForeignKey('users_user.id'))
