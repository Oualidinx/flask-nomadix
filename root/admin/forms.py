from flask_wtf import FlaskForm
#from wtforms.fields.choices import SelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from wtforms import SubmitField, StringField, PasswordField, SelectField

from root.models import User
import re
name_regex = re.compile('^[a-zA-Z]+$')

class RegistrationForm(FlaskForm):
    first_name = StringField('Nom: ', validators=[DataRequired('Champs obligatoire')])
    last_name = StringField('Prénom: ', validators=[DataRequired('Champs obligatoire')])
    username = StringField('Email: ', validators=[DataRequired('Champs obligatoire')])
    password = PasswordField('Mot de passe:', validators=[DataRequired('Champs obligatoire')])
    role = SelectField('Role:', choices=[('master','Master'), ('financier', 'Financier'),
                                         ('gestionnaire','Gestionnaire'),('commerçial','Commerçial')],
                       validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer Mot de passe:', validators=[DataRequired('Champs obligatoire'),
                                                                            EqualTo('password',
                                                                            message="Vérifier bien ce champs S.V.P")])
    submit = SubmitField('Créer le compte')

    def validate_first_name(self, first_name):
        if name_regex.search(first_name.data) is None:
            raise ValidationError('Nom Invalide')

    def validate_last_name(self, last_name):
        if name_regex.search(last_name.data) is None:
            raise ValidationError('Prénom Invalide')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom est déjà utilisé')


class UpdateInfoForm(FlaskForm):
    first_name = StringField('Nom: ')
    last_name = StringField('Prénom: ')
    username = StringField('Nom d\'utilisateur: ')
    password = PasswordField('Mot de passe:')
    confirm_password = PasswordField('Confirmer Mot de passe:', validators=[EqualTo('password',
                                                                            message="Vérifier bien ce champs S.V.P")])
    submit = SubmitField('Mise à jour')

    def validate_first_name(self, first_name):
        if name_regex.search(first_name.data) is None:
            raise ValidationError('Nom Invalide')

    def validate_last_name(self, last_name):
        if name_regex.search(last_name.data) is None:
            raise ValidationError('Prénom Invalide')