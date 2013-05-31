from flask import (Blueprint, request, render_template, flash, g, session,
    redirect, url_for)
from werkzeug import check_password_hash, generate_password_hash

from deploystream import db
from deploystream.apps.users.forms import RegisterForm, LoginForm
from deploystream.apps.users.models import User
from deploystream.apps.users.decorators import requires_login

mod = Blueprint('users', __name__, url_prefix='/users')


@mod.route('/me/')
@requires_login
def home():
    return render_template("users/profile.html", user=g.user)


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # we use werzeug to validate user's password
        if user and check_password_hash(user.password, form.password.data):
            # the session can't be modified as it's signed,
            # it's a safe place to store the user id
            session['user_id'] = user.id
            flash('Welcome %s' % user.name)
            return redirect(url_for('users.home'))
        flash('Wrong email or password', 'error-message')
    return render_template("users/login.html", form=form)


@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registration Form
    """
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        print "VALID"
        # create an user instance not yet stored in the database
        user = User(form.name.data, form.email.data, \
        generate_password_hash(form.password.data))
        # Insert the record in our database and commit it
        db.session.add(user)
        db.session.commit()

        # Log the user in, as he now has an id
        session['user_id'] = user.id

        # flash will display a message to the user
        flash('Thanks for registering')
        # redirect user to the 'home' method of the user module.
        return redirect(url_for('users.home'))
    else:
        print form.__dict__
    return render_template("users/register.html", form=form)
