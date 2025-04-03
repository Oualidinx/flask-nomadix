from flask_wtf import FlaskForm
from wtforms.fields.form import FormField
from decimal import Decimal
from wtforms.fields.numeric import IntegerField
from wtforms.fields import DateField
from wtforms.fields.simple import BooleanField
from wtforms.form import Form
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length, NumberRange, Optional
from wtforms import SubmitField, StringField, PasswordField, SelectField, FieldList
import re
from root.models import Hotel, Bus, Guide, Agency

name_regex = re.compile('^[a-z A-Z]+$')
phone_number_regex = re.compile('^[\+]?[(]?[0-9]{2}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,7}$')

class RegistrationForm(FlaskForm):
    first_name = StringField('Nom: ', validators=[DataRequired('Champs obligatoire')])
    last_name = StringField('Prénom: ', validators=[DataRequired('Champs obligatoire')])
    # username = StringField("Nom d'utilisateur: ", validators=[DataRequired('Champs obligatoire')])
    # password = PasswordField('Mot de passe:', validators=[DataRequired('Champs obligatoire')])
    role = SelectField('Rôle:', choices=[(None, 'Sélectionner un rôle'), ('master','Master'),
                                         ('financier', 'Financier'),
                                         ('gestionnaire','Gestionnaire'),('commercial','Commerçial')],
                       validators=[DataRequired()])
    submit = SubmitField('Créer le compte')

    def validate_first_name(self, first_name):
        if name_regex.search(first_name.data) is None:
            raise ValidationError('Nom Invalide')

    def validate_last_name(self, last_name):
        if name_regex.search(last_name.data) is None:
            raise ValidationError('Prénom Invalide')

    # def validate_username(self, username):
    #     user = User.query.filter_by(username=username.data).filter_by(is_deleted=False).first()
    #     if user:
    #         raise ValidationError('Ce nom est déjà utilisé')

    def validate_role(self, role):
        # user = User.query.filter_by(username=role.data).first()
        if role.data == None:
            raise ValidationError('rôle invalide')


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


class ContactForm(FlaskForm):
    name = StringField('Etiquette: ', validators=[DataRequired('Champs obligatoire'),])
    email = StringField('Email: ')
    phone = StringField('Numéro de téléphone: ', validators=[DataRequired('Champs obligatoire'),])
    address = StringField('Adresse: ')
    city = StringField('Ville: ')
    state = StringField('Wilaya')
    add = SubmitField('Envoyer')


class HotelForm(FlaskForm):
    name =StringField('Nom: ', validators=[DataRequired('Champs obligatoire')])
    star_rating = IntegerField('Rating: ', validators=[DataRequired()])
    phone_number = StringField("Numéro de téléphone: ",
                               validators=[DataRequired('Champs obligatoire'), Length(min=9, max=10)])
    state = StringField('Ville: ', validators=[DataRequired('Champs obligatoire')])
    submit = SubmitField('Valider')
    def validate_name(self, name):
        if name and name_regex.search(name.data) is None:
            raise ValidationError('Nom Invalide')

    def validate_start_rating(self, start_rating):
        if int(start_rating.data) < 1 or int(start_rating.data) > 5:
            raise ValidationError('Rating invalide')

    def validate_phone_number(self, phone_number):
        if phone_number and phone_number_regex.search(phone_number.data) is None:
            raise ValidationError('Numéro de téléphone invalide')


class BusForm(FlaskForm):
    company = StringField('Nom de la societé ', validators=[DataRequired('Champs obligatoire')])
    driver_full_name = StringField('Nom du conducteur ', validators=[DataRequired('Champs obligatoire')])
    capacity = IntegerField('Nombre de place du Bus ',validators=[DataRequired('Champs obligatoire'), NumberRange(min=1, max=100)])
    state = StringField('Wilaya: ')
    drivers_phone_number = StringField('Numéro de téléphone du conducteur ', validators=[DataRequired('Champs obligatoire')])
    submit = SubmitField('Valider')

    def validate_driver_full_name(self, driver_full_name):
        if driver_full_name and name_regex.search(driver_full_name.data) is None:
            raise ValidationError('Nom Invalide')

    def validate_capacity(self, capacity):
        if capacity.data > 100:
            raise ValidationError('Nombre de place du Bus invalide')

    def validate_phone_number(self, phone_number):
        if phone_number and phone_number_regex.search(phone_number.data) is None:
            raise ValidationError('Numéro invalide')

from root.models import User, Contact
class GuideForm(FlaskForm):
    full_name = StringField('Nom complet: ', validators=[DataRequired('Champs obligatoire')])
    sex = SelectField('Genre: ', choices=[(None,'Sélectionner ...'),('homme', 'Homme'), ('femme', 'Fêmme')], validators=[DataRequired()])
    state = SelectField('Wilaya: ', validate_choice=False)
    guide_phone_number=StringField('Numéro de téléphone:', validators=[DataRequired('Champs obligatoire')])
    submit = SubmitField('Valider')

    def validate_full_name(self, full_name):
        if full_name and name_regex.search(full_name.data) is None:
            raise ValidationError('Nom Invalide')

    def validat_state(self, state):
        if state and name_regex.search(state.data) is None:
            raise ValidationError('Wilaya Invalide')

    def validate_guide_phone_number(self, guide_phone_number):
        if guide_phone_number and phone_number_regex.search(guide_phone_number.data) is None:
            raise ValidationError('Numéro invalid')
        contact =Contact.query.filter_by(phone=guide_phone_number.data).first()
        if contact :
            guide = Guide.query.filter_by(id=contact.fk_guide_id).first()
            if guide and guide.is_deleted==False:
                raise ValidationError('Numéro existe déjà')

    def validate_state(self, state):
        if state.data=='None':
            raise ValidationError("Sélectionner la wilaya")

from datetime import datetime
class VoyagesForm(FlaskForm):
    destination = StringField("Destination", validators=[DataRequired('Champs obligatoire')])
    date_depart = DateField('Date de la départ', validators=[DataRequired()])
    subscription_due_date=DateField('Date de clôture des inscriptions', validators=[DataRequired()])
    date_end = DateField("Date d'arrivée", validators=[DataRequired()])
    hotel_fees = IntegerField("Frais d'hôles", default=0, validators=[Optional()])
    nb_places = IntegerField("Nombre de places", default=0, validators=[DataRequired(), NumberRange(min=1, max=200)])
    bus_company = QuerySelectField('Bus',
                                   allow_blank=True,
                                   blank_text="Sélectionner le bus",
                                   query_factory=lambda : Bus.query.filter_by(is_deleted=False).all(),
                                   validators=[Optional()])
    hotel = QuerySelectField("Nom de l'hôtel: ",
                             query_factory=lambda : Hotel.query.filter_by(is_deleted=False).all(),
                             validators=[Optional()])
    guides = QuerySelectField('Guides',
                              allow_blank=True,
                              blank_text="Sélectionner le guide...",
                              query_factory=lambda : Guide.query.filter_by(is_deleted=False).all(),
                              validators=[Optional()])
    bus_fees = IntegerField('Frais de bus', default=0, validators=[Optional()])
    visa_fees =IntegerField("Frais de visa", default=0, validators=[Optional()])
    guide_fees = IntegerField('Frais de guide', default=0, validators=[Optional()])
    avion_fees = IntegerField("Frais de billets d'avion", default=0, validators=[Optional()])
    is_plane_included = BooleanField('Le voyage inclut-il un vol en avion ?', default=False)
    is_bus_included = BooleanField('Le voyage inclut-il un bus ?', default=False)
    is_hotel_included = BooleanField('Le voyage inclut-il un hôtel ?', default = False)
    is_guide_included = BooleanField('Le voyage inclut-il un guide ?', default=False)

    submit = SubmitField('Valider')

    def validate_destionation(self, destination):
        if destination and name_regex.search(destination.data) is None:
            raise ValidationError('Nom Invalide')

    def validate_date_depart(self, date_depart):
        # print(date_depart.data)
        # print(date_depart.data <= datetime.utcnow().date())
        if date_depart.data:
            if date_depart.data <= datetime.utcnow().date():
                raise ValidationError('Date de départ non valide')

    def validate_date_end(self, date_end):

        if date_end.data:
            if date_end.data <= datetime.utcnow().date():
                raise ValidationError('Date de retour non valide')

        if self.date_depart.data:
            if self.date_depart.data > date_end.data:
                raise ValidationError('Date de retour non valide par rapport à la date de départ')

    def validate_subscription_due_date(self, subscription_due_date):
        if subscription_due_date.data:
            if subscription_due_date.data <= datetime.utcnow().date():
                raise ValidationError('Date d\'expiration non valide')

        if self.date_depart.data:
            if self.date_depart.data <= subscription_due_date.data:
                raise ValidationError('Date de clôture des inscrptions non valide')
        if self.date_end.data:
            if subscription_due_date.data > self.date_end.data:
                raise ValidationError('Date de clôture des inscrptions non valide')


class PersonForm(Form):
    first_name = StringField('Nom', validators=[DataRequired()])
    last_name = StringField('Prénom', validators=[DataRequired()])
    sexe = SelectField('Genre', choices=[('m', 'Male'), ("f", "femelle")], validators=[DataRequired()])
    phone_number = StringField('Numéro de téléphone')
    delete_entry = SubmitField('Supprimer')

    def validate_contact(self, phone_number):
        if phone_number and phone_number_regex.search(phone_number.data) is None:
            raise ValidationError('Numéro de téléphone invalide')

    def validate_first_name(self, first_name):
       if first_name and name_regex.search(first_name.data) is None:
            raise ValidationError('Nom Invalide')

    def validate_last_name(self, last_name):
        if last_name and name_regex.search(last_name.data) is None:
            raise ValidationError('Prénom Invalide')


class Subscription(FlaskForm):
    label = StringField('Titre:')
    responsible_full_name=StringField('Nom de représentant: ', validators=[DataRequired()])
    reserved_places = IntegerField('Nombres de places: ', validators=[DataRequired(), NumberRange(min=1)])
    phone_number = StringField('Numéro de téléphone: ', validators=[DataRequired('Champs obligatoire')])
    persons = FieldList(FormField(PersonForm), min_entries=1)
    add = SubmitField('add new line')
    fin = SubmitField('Enregistrer')
    submit = SubmitField('Valider')

    def validate_phone_number(self, phone_number):
        if phone_number and phone_number_regex.search(phone_number.data) is None:
            raise ValidationError('Numéro invalide')

    def validate_responsible_full_name(self, responsible_full_name):
        if responsible_full_name and name_regex.search(responsible_full_name.data) is None:
            raise ValidationError('Nom Invalide')

from root.models import VoyageForAgency
class PaymentForm(FlaskForm):
    group_id = SelectField('ID Groupe: ', validate_choice=False)
    rest_to_pay=StringField('Reste à payer (DZD) ')
    montant_verse = StringField('Montant versé (DZD)')
    versement = StringField('Versement (DZD)', validators=[DataRequired()])
    submit = SubmitField('Envoyer')
    def validate_group_id(self, group_id):
        if not group_id.data:
            raise ValidationError('Veuillez sélectionner d\'abord le group')
        group = Agency.query.get(group_id.data)
        if not group:
            raise ValidationError("ID group n'est pas reconnu")


    def validate_montant_verse(self, montant_verse):
        verse = float(Decimal(re.sub(r'[^\d.]', '', montant_verse.data)))
        if verse<0:
            raise ValidationError('Montant verse invalide')

    def validate_versement(self, versement):
        if float(versement.data)<0:
            raise ValidationError('Versement invalide')

        v_for_a = VoyageForAgency.query.filter_by(fk_agency_id=int(self.group_id.data)).first()

        rest = float(Decimal(re.sub(r'[^\d.]', '', self.rest_to_pay.data)))
        verse = float(Decimal(re.sub(r'[^\d.]', '', self.montant_verse.data)))
        if v_for_a:
            if float(versement.data)>(rest+verse):
                raise ValidationError('Vérifier la valeur saisie dans ce champ')

