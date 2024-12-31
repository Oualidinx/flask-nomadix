from root import database as db
from flask_login import UserMixin

from datetime import datetime
import json

class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)


class User(UserMixin, db.Model):
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    role = db.Column(db.String(20))
    is_deleted = db.Column(db.Boolean, default=0)
    password_hasChanged = db.Column(db.Boolean, default = False)
    username = db.Column(db.String(100), nullable = False)
    phone_number = db.Column(db.String(10), default="champ vide")
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'USER: <{self.username}, {self.first_name}, {self.last_name}> \n'

    def repr(self, columns=None):
        _dict = {
            'id': self.id,
            'full_name': self.first_name+" "+self.last_name,
            'username': self.username,
            'role': self.role,
            'phone_number': self.phone_number
        }
        return {key: _dict[key] for key in columns} if columns else _dict


class Voyage(db.Model):
    __tablename__="voyage"
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    subscription_due_date=db.Column(db.DateTime, default=datetime.now())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_depart = db.Column(db.DateTime, default=datetime.utcnow)
    date_end = db.Column(db.DateTime, default=datetime.utcnow)
    hotel_fees = db.Column(db.Integer, default=0)
    # bus_company = db.Column(db.String(100))
    bus_fees = db.Column(db.Integer, default=0)
    visa_fees = db.Column(db.Integer, default=0)
    guide_fees = db.Column(db.Integer, default=0)
    plane_fees = db.Column(db.Integer, default=0)
    is_plane_included = db.Column(db.Boolean, default=0)
    is_guide_included = db.Column(db.Boolean, default=0)
    is_hotel_included = db.Column(db.Boolean, default=0)
    is_bus_included = db.Column(db.Boolean, default=0)
    is_visa_included = db.Column(db.Boolean, default=0)
    includes = db.relationship('Include', backref="travel_include", lazy="subquery")
    agencies = db.relationship("Agency", secondary="voyage_agency",
                               viewonly=True,
                            primaryjoin="Agency.id == "
                                        "foreign(VoyageForAgency.fk_agency_id)",
                            secondaryjoin="Voyage.id == "
                                          "foreign(VoyageForAgency.fk_voyage_id)")
    invoices = db.relationship('Invoice', backref="voyage_invoices", lazy="subquery")


    def repr(self, columns=None):
        _dict={
            "id": self.id,
            "destination": self.destination,
            "created_at":self.created_at,
            "created_by":User.query.get(self.created_by).first_name+" "+User.query.get(self.created_by).last_name,
            "date_depart":self.date_depart.date(),
            "subscription_due_date":self.subscription_due_date.date(),
            "date_end":self.date_end.date(),
            "hotel_fees":"{:,.2f}".format(self.hotel_fees) if self.is_hotel_included else 0,
            "bus_company": Bus.query.get(self.includes[0].fk_bus_id) if len(self.includes)>0 and self.includes[0].fk_bus_id else "",
            "bus_fees":"{:,.2f}".format(self.bus_fees) if self.is_bus_included else 0,
            "visa_fees":"{:,.2f}".format(self.visa_fees) if self.is_visa_included else 0,
            "guide_fees":"{:,.2f}".format(self.guide_fees) if self.is_guide_included else 0,
            "guide_full_name":Guide.query.get(self.includes[0].fk_guide_id) if len(self.includes) > 0 and self.includes[0].fk_guide_id else "",
            "hotel_name":Hotel.query.get(self.includes[0].fk_hotel_id) if len(self.includes) > 0 and self.includes[0].fk_hotel_id else "",
            "plane_fees":"{:,.2f}".format(self.plane_fees) if self.is_plane_included else 0,
            "is_plane_included":"inclue" if self.is_plane_included else "exclu",
            "is_guide_included":"inclue" if self.is_guide_included else "exclu",
            "is_hotel_included":"inclue" if self.is_hotel_included else "exclu",
            "is_bus_included":"inclue" if self.is_bus_included else "exclu",
            "is_visa_included":"inclue" if self.is_visa_included else "exclu",
            "agencies":[agency.repr() for agency in self.agencies]
        }
        return {key: _dict[key] for key in columns} if columns else _dict

class Bus(db.Model):
    __tablename__="bus"
    id=db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    driver_full_name = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    state = db.Column(db.String(100), nullable = True)
    is_deleted = db.Column(db.Boolean, default=0)
    contacts = db.relationship('Contact', backref="bus_contact", lazy='subquery')
    voyages = db.relationship('Voyage', secondary="include",viewonly=True,
                            primaryjoin="Bus.id == foreign(Include.fk_bus_id)",
                            secondaryjoin="Voyage.id == foreign(Include.fk_voyage_id)")
    def __repr__(self):
        return f'{self.company}'

    def repr(self, columns=None):
        _dict = {
            'id': self.id,
            'driver_full_name': self.driver_full_name,
            'capacity': self.capacity,
            'company': self.company,
            'contacts': [contact.repr() for contact in self.contacts]
        }
        return {key: _dict[key] for key in columns} if columns else _dict




class Contact(db.Model):
    __tablename__ =  "contact"
    id=db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    fk_bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
    fk_guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
    fk_hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))
    fk_agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))
    fk_person_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def __repr__(self):
        return (f'Contact: {self.name}, '
                f'email={self.email}, '
                f'phone={self.phone}, '
                f'address={self.address}'
                f'city={self.city}, '
                f'state={self.state}, '
                f'is_deleted={self.is_deleted}')

    def repr(self, columns=None):
        _dict = {
                'name': self.name,
                'email': self.email,
                'phone':self.phone,
                'address':self.address,
                'city':self.city,
                'state':self.state,
                'is_deleted':self.is_deleted}
        return {key: _dict[key] for key in columns} if columns else _dict


class Guide(db.Model):
    __tablename__ = "guide"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=False)
    sex = db.Column(db.String(10))
    state = db.Column(db.String(100), nullable=True)
    contacts = db.relationship('Contact', backref="guide_contact", lazy='subquery')
    voyages = db.relationship('Voyage', secondary="include",viewonly=True,
                            primaryjoin="Guide.id == foreign(Include.fk_guide_id)",
                            secondaryjoin="Voyage.id == foreign(Include.fk_voyage_id)")

    def __repr__(self):
        return f'{self.name}'

    def repr(self, columns=None):
        _dict = {
            'id':self.id,
            'name': self.name,
            'sex': self.sex,
            '#voyages': len(self.voyages),
            'voyages':self.voyages}
        return {key: _dict[key] for key in columns} if columns else _dict


class Hotel(db.Model):
    __tablename__ = "hotel"
    id = db.Column(db.Integer, primary_key=True)
    is_deleted = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(100))
    contacts = db.relationship('Contact', backref="hotel_contact", lazy='subquery')
    star_rating = db.Column(db.Integer, default=0)
    state = db.Column(db.String(100))
    voyages = db.relationship('Voyage', secondary="include", viewonly=True,
                              primaryjoin="Hotel.id == foreign(Include.fk_hotel_id)",
                              secondaryjoin="Voyage.id == foreign(Include.fk_voyage_id)")
    def __repr__(self):
        return f'{self.name}'

    def repr(self, columns=None):
        _dict = {
            'id': self.id,
            'name': self.name,
            'is_deleted': self.is_deleted,
            'star_rating': self.star_rating,
            "#voyages":len(self.voyages) if len(self.voyages)>0 else "/",
            "voyages":[v.repr() for v in self.voyages],
            'contacts': [c.repr() for c in self.contacts]
        }
        return {key: _dict[key] for key in columns} if columns else _dict



class Agency(db.Model):
    __tablename__ = "agency"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    reserved_places= db.Column(db.Integer, default=0)
    contacts = db.relationship('Contact', backref="agency_contact", lazy='subquery')
    persons = db.relationship('Person', backref="agency_persons", lazy="subquery")

    def __repr__(self):
        return f'{self.label}, Contacts: {self.contacts}'


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    payments = db.relationship('Payment', backref='payments_invoice', lazy='subquery')
    fk_voyage_id = db.Column(db.Integer, db.ForeignKey('voyage.id'))
    fk_agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))
    invoice_type = db.Column(db.String(100))
    entities = db.relationship('Entity', backref='invoice_entities', lazy='subquery')

    def __repr__(self):
        return (f'Date de facture={self.date},'
                f'Montant= {self.amount}, '
                f'Voyage={Voyage.query.get(self.fk_voyage_id)},'
                f'Agency={Agency.query.get(self.fk_agency_id)}, '
                f'Payments={self.payments}')


class Payment(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(db.Integer)
    type = db.Column(db.String(100))
    fk_invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __repr__(self):
        return f'Date de payment={self.date}, Montant={self.amount}'


class Person(db.Model):
    __tablename__ = "person"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    contacts = db.relationship('Contact', backref="person_contact", lazy='subquery')
    fk_agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))


class Include(db.Model):
    __tablename__ = "include"
    id = db.Column(db.Integer, primary_key=True)
    fk_voyage_id = db.Column(db.Integer, db.ForeignKey('voyage.id'))
    fk_guide_id = db.Column(db.Integer, db.ForeignKey('guide.id'))
    fk_bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'))
    fk_hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'))

class VoyageForAgency(db.Model):
    __tablename__ = "voyage_agency"
    id = db.Column(db.Integer, primary_key=True)
    fk_agency_id = db.Column(db.Integer, db.ForeignKey('agency.id'))
    fk_voyage_id = db.Column(db.Integer, db.ForeignKey('voyage.id'))
    total_paid=db.Column(db.Integer, default = 0)
    rest_to_pay=db.Column(db.Integer, default = 0)

    def __repr__(self, columns=None):
        return None

class Entity(db.Model):
    __tablename__ = "entity"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    is_deleted = db.Column(db.Boolean, default=0)
    montants = db.Column(db.Integer)
    unit = db.Column(db.String(100))
    quantity = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Integer,default=0)
    fk_invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'))

    def __repr__(self):
        return f'{self.label}, {self.montants}, {self.unit}, {self.quantity}, {self.total_amount}'

