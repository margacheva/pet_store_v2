from flask_babel import gettext
from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired


class EmailSenderForm(FlaskForm):
    email = EmailField(gettext("Email", validators=[DataRequired]))
    submit = SubmitField(gettext("Submit"))
