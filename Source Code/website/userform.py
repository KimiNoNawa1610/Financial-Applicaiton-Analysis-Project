from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    firstname = StringField('firstname',validators=[DataRequired()])
    lastname = StringField('lastname',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])
    submit = SubmitField("Submit")

class StockForm(FlaskForm):
    stockname = StringField('stockname',validators=[DataRequired()])
    stockprice = StringField('stockprice',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])
    submit = SubmitField("Submit")