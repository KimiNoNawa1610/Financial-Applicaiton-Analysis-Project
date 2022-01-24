from . import db # from the package, import the db instance
from flask_login import UserMixin
from sqlalchemy.sql import func 


# a layout for the stock name that store in the database
class Stock(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    user_id =db.Column(db.Integer, db.ForeignKey('user.id'))


#user object (table)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(150))
    stocks = db.relationship('Stock')


