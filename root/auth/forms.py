from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField
from wtforms.validators import DataRequired, ValidationError

from root.models import User
import re

price_letters_regex = re.compile('^[a-zA-Z-]')
phone_number_regex = re.compile('^[\+]?[(]?[0-9]{2}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,7}$')

class LoginForm(FlaskForm):
    username = StringField('Nom d\'utilisateur: ', validators=[DataRequired()])
    password = PasswordField('Mot de passe: ', validators=[DataRequired()])
    submit = SubmitField('Se connecter')
    def validate_email(self, username):

        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Veuillez vérifier vos informations')



