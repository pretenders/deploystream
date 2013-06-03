from flask.ext.wtf import (
    Form, TextField, PasswordField, BooleanField, RecaptchaField
)
from flask.ext.wtf import Required, Email, EqualTo


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
