from flask.ext.wtf import (
    Form, TextField, PasswordField, BooleanField, RecaptchaField
)
from flask.ext.wtf import Required, Email, EqualTo

from .models import User


class LoginForm(Form):
    username = TextField('Username', [Required()])
    password = PasswordField('Password', [Required()])


class RegisterForm(Form):
    username = TextField('Username', [Required()])
    email = TextField('Email address', [Email()])
    password = PasswordField('Password', [Required()])
    confirm = PasswordField('Repeat Password', [
      Required(),
      EqualTo('password', message='Passwords must match')
      ])
    accept_tos = BooleanField('I accept the TOS', [Required()])
    #recaptcha = RecaptchaField()

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        uname_clash = User.query.filter_by(username=self.username.data).first()
        if uname_clash:
            self.username.errors.append("This username is already in use.")
            return False

        return True
