from flask_login import current_user
from . import db
from .models import Stock, User, UserStock
from flask import flash, request
import yfinance as yf
import time
import json
import smtplib


searched = 'aapl'


def getStockPrice1d(stock):
    # print(stock)
    info = yf.Ticker(stock)
    return info.info['regularMarketPrice']

# print(getStockPrice1d("TSLA"))

stock_test = 'aapl'
target_price_test = 100

new_price_target = UserStock(name = stock_test, target_price = target_price_test, user_id = current_user.id)
db.session.add(new_price_target)
db.session.commit()
flash("target price added", category = "success")

stock = json.loads(request.data)
stockId = stock['stockId']
stock = Stock.query.get(stockId)
UserStock = json.loads(request.data)
if (stock):
    if (UserStock.user_id == current_user.id and UserStock.stock_id == stock):
        targetPrice = UserStock['targetPrice']
        target_price = UserStock.query.get(targetPrice)

def checkStock(searched):
    alertPrice = getStockPrice1d(searched)
    alertValue = alertPrice
    if alertValue < target_price: #modify number for user options in seconds
        #send email if price goes under 100, this number is abitrary for testing
        send_email()

def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('throwaway246abc@gmail.com', 'throwit246abc') #sender email
    subject = 'Price has fallen under $100'
    body = 'Price down'
    msg = f'subject: {subject} {body}'

    server.sendmail( #change email to use the user's email
        'throwaway246abc@gmail.com', #sender
        'throwaway246abc@gmail.com', #receiver 
        msg
    )

    server.quit()

#this form of email sending can only send emails to gmail that have
#less secure apps allowed to recieve emails from
#otherwise gmail will block it

while(True):
    checkStock(searched)
    # time.sleep(10)
    # 1800 is 30 minutes