from flask import (Blueprint, request, render_template, flash, g, session,
    redirect, url_for)
from werkzeug import check_password_hash

from .forms import RegisterForm, LoginForm
from .models import User
from .lib import load_user_to_session
from .decorators import requires_login


mod = Blueprint('users', __name__, url_prefix='/users')


@mod.before_request
def before_request():
    """
    pull user's profile from the database before every request are treated
    """
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])


@mod.route('/me/')
@requires_login
def home():
    return redirect('/api/users/{0}'.format(g.user.id))


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Login form
    """
    form = LoginForm(request.form)
    # make sure data are valid, but doesn't validate password is right
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # we use werzeug to validate user's password
        if user and check_password_hash(user.password, form.password.data):
            load_user_to_session(session, user)

            flash('Welcome %s' % user.username)
            return redirect(url_for('users.home'))
        flash('Wrong email or password', 'error-message')
    if request.method == 'POST':
        suffix = ".html"
    else:
        suffix = "_ajax.html"

    return render_template("users/login" + suffix, form=form)


@mod.route('/register/', methods=['GET', 'POST'])
def register():
    """
    Registration Form
    """
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # create a user instance not yet stored in the database
        user = User.create_user(
            form.username.data,
            form.email.data,
            form.password.data
        )

        # Log the user in, as he now has an id
        load_user_to_session(session, user)

        # flash will display a message to the user
        flash('Thanks for registering')
        # redirect user to the 'home' method of the user module.
        return redirect(url_for('users.home'))

    return render_template("users/register.html", form=form)
