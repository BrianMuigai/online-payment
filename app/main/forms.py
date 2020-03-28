from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField, \
SelectField, PasswordField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l

class MakePayment(FlaskForm):
    mobile = StringField(_('Mpesa Number'), validators=[DataRequired()])
    charges = StringField(_('Amount'), validators=[DataRequired()])
    

