from unicodedata import category
from flask import Blueprint, jsonify, render_template, request, flash, jsonify, redirect, url_for
from flask_login import  login_required, current_user
from .models import Stock, User
from . import db
from .fy import getStockPrice1d, getCurrentPrice
from .searchform import SearchForm
import json
from .userform import UserForm
from flask_mail import Mail, Message
from . import mail
import yfinance as yf
import time
import smtplib
import requests

def checkStock(searched):
    alertPrice = getStockPrice(searched)
    alertValue = alertPrice
    if alertPrice < 100: #modify number for user options
        #send email if price goes under 100, this number is abitrary for time being
        send_email()

def send_email(password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('TempEmailHere', password)
    subject = 'Price has fallen under $100'
    body = 'Price down'
    msg = f'subject: {subject} {body}'

    server.sendmail(
        'senderEmailHere',
        'ReceiverEmailHere',
        msg
    )

    server.quit()

#this form of email sending can only send emails to gmail that have
#less secure apps allowed to recieve emails from
#otherwise gmail will block it

while(True):
    checkStock(searched)
    time.sleep(1800)