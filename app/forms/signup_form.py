from flask_babel import gettext
from flask_wtf import FlaskForm
from wtforms import (EmailField, PasswordField,
                     SubmitField)
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField(gettext("Email", validators=[DataRequired()]))
    password = PasswordField(gettext("Password", validators=[DataRequired()]))
    submit = SubmitField(gettext("Submit"))
