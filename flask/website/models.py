from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')

class ProfileData(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50))
    address_1 = db.Column(db.String(100))
    address_2 = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    in_state_status = True
    if state != "TX":
        in_state_status = False
    zip_code = db.db.Column(db.String(9))