from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db=SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__='user'
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,nullable=False)
    password=db.Column(db.String,nullable=False)
    role=db.Column(db.String,nullable=False)
    phone=db.Column(db.String)
    address=db.Column(db.String)
    status=db.Column(db.String,default='active')
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    bookings=db.relationship('Booking',backref='trekker',cascade='all, delete-orphan')
    staff_profile=db.relationship('StaffProfile',backref='trekker',cascade='all, delete-orphan')

    def get_id(self):
        return str(self.email)

class StaffProfile(db.Model):
    __tablename__='staff_profile'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    bio=db.Column(db.String)
    exp_years=db.Column(db.Integer,default=0)
    status=db.Column(db.String,default='pending')

    treks=db.relationship('Trek',backref='assigned_staff',lazy=True)

class Trek(db.Model):
    __tablename__='trek'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    location=db.Column(db.String,nullable=False)
    difficulty=db.Column(db.String,nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    total_slots=db.Column(db.Integer,nullable=False)
    available_slots=db.Column(db.Integer,nullable=False)
    status=db.Column(db.String,default='Pending')
    start_date=db.Column(db.Date,nullable=False)
    end_date=db.Column(db.Date,nullable=False)
    description=db.Column(db.String)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff_profile.id'), nullable=True)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='trek', cascade='all, delete-orphan', lazy=True)

class Booking(db.Model):
    __tablename__='booking'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    trek_id=db.Column(db.Integer,db.ForeignKey('trek.id'),nullable=False)
    booking_date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String,default='Booked')
    payment_status=db.Column(db.String,default='Pending')