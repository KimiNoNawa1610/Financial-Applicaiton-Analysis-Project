import smtplib 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class sendemail(FlaskForm):

    useremail = StringField('Email Address')
    message = StringField('Alert')

    emailsender = smtplib.SMTP('placeholder@gmail.com, PORTNUMBER')
    emailsender.starttls() 

    emailsender.login('placeholder@gmail.com', 'placeholderemailPW')
    emailsender.sendmail('placeholder@gmail.com', useremail, message)
    submit = SubmitField("Submit")


    
