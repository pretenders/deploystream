from deploystream import db
from deploystream.apps.base.models import Base


user_repo_permissions = db.Table('repo_permissions',
    db.Column("user_id", db.Integer, db.ForeignKey('users_user.id')),
    db.Column("repo_id", db.Integer, db.ForeignKey('repo_repo.id'))
)


class Repo(db.Model, Base):

    EXCLUDE_AT_API = ['users']

    __tablename__ = 'repo_repo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    git_url = db.Column(db.String(200), unique=True)
    active = db.Column(db.Boolean())

    users = db.relationship('User', secondary=user_repo_permissions,
                            backref='repos')
