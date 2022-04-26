from . import db # from the package, import the db instance
from flask_login import UserMixin
from sqlalchemy.sql import func 

#sqllite 
# a layout for the stock name that store in the database
class Stock(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique = True)
    price = db.Column(db.BigInteger())
    

#user object (table)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    password = db.Column(db.String(150))
    stocks = db.relationship('UserStock')


class UserStock(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), primary_key = True)
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    rating = db.Column(db.Integer,default=0)
    number_of_stock = db.Column(db.Integer) #calculated column

class Comment(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stock.id'), primary_key = True)
    date = db.Column(db.DateTime(timezone = True), default = func.now(), primary_key = True)
    comment = db.Column(db.String(500))
