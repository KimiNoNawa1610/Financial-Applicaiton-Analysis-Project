import yfinance as yf
import time
import smtplib
from threading import *


# searched = 'aapl'
# change the searched to match the stock that is being applied to the profile


def getStockPrice1d(stock):
    # print(stock)
    info = yf.Ticker(stock)
    return info.info['regularMarketPrice']

# print(getStockPrice1d("TSLA"))

def checkStock(searched,target_price, email):
    alertValue = getStockPrice1d(searched)
    if alertValue < target_price: #modify number for user options in seconds
        #send email if price goes under 100, this number is abitrary for testing
        send_email(email,searched,target_price)

def send_email(email, searched, target_price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('throwaway246abc@gmail.com', 'throwit246abc') #sender email
    subject = 'Price alert for '+searched
    body = 'Price has of '+searched+' reached the of $'+target_price
    msg = f'subject: {subject} {body}'

    server.sendmail( #change email to use the user's email
        'throwaway246abc@gmail.com', #sender
        email, #receiver 
        msg
    )

    server.quit()

#this form of email sending can only send emails to gmail that have
#less secure apps allowed to recieve emails from
#otherwise gmail will block it

def thread_1(searched,target_price, email):               
    while(True):
        checkStock(searched,target_price, email)
        time.sleep(1800)
        # 1800 is 30 minutes

T = Thread(daemon = True, target=thread_1, args=["appl",200,"vothanhnhan108@gmail.com"])
                
# starting of thread T
T.start()     
 
                 

