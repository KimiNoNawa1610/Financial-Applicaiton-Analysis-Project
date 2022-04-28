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

<<<<<<< Updated upstream
# def checkStock(searched,target_price, email):
#     alertValue = getStockPrice1d(searched)
#     if alertValue < target_price: #modify number for user options in seconds
#         #send email if price goes under 100, this number is abitrary for testing
#         send_email(email,searched,target_price)

=======
def checkStock(searched,target_price, email):
    alertValue = 0
    alertValue = getStockPrice1d(searched)
    if alertValue < target_price: #modify number for user options in seconds
        #send email if price goes under 100, this number is abitrary for testing
        send_email(email,searched,target_price)
>>>>>>> Stashed changes

def send_email(email, searched, target_price):
    alertValue = getStockPrice1d(searched)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('throwaway246abc@gmail.com', 'throwit246abc') #sender email
    subject = 'Price alert for '+searched
    if alertValue < target_price:
        body = f'Price of {searched} is less than ${str(target_price)}\nPrice: ${alertValue}'
    elif alertValue > target_price:
        body = f'Price of {searched} is greater than ${str(target_price)}\nPrice: ${alertValue}'
    else:
        body = f'Price of {searched} is equal to ${str(target_price)}\nPrice: ${alertValue}'
    msg = f'subject: {subject} \n{body}'

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
        send_email(email, searched, target_price)
        time.sleep(1800)
        # 1800 is 30 minutes
<<<<<<< Updated upstream

# T = Thread(daemon = True, target=thread_1, args=["aapl",200,"@gmail.com"])
                
# starting of thread T
# T.start()     
=======
  
>>>>>>> Stashed changes
 
                 

