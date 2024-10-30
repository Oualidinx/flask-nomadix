from root import database as db
from flask_login import UserMixin

from datetime import datetime, timedelta
import json, jwt
from time import time
from root import app
from root import login_manager
from flask import current_app

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
    phone_number = db.Column(db.String(10))
    password_hash = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return '<User %r %r %r>' % self.username, self.first_name, self.last_name

    def repr(self, columns=None):
        _dict = {
            'id': self.id,
            'full_name': self.first_name+" "+self.last_name,
            'username': self.username,
            'role': self.role,
            'phone_number': self.phone_number
        }
        return {key: _dict[key] for key in columns} if columns else _dict

