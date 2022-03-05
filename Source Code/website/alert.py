import yfinance as yf
import time
import smtplib

# searched = 'aapl'


def getStockPrice1d(stock):
    # print(stock)
    info = yf.Ticker(stock)
    return info.info['regularMarketPrice']

# print(getStockPrice1d("TSLA"))

def checkStock(searched):
    alertPrice = getStockPrice1d(searched)
    alertValue = alertPrice
    if alertValue < 1000: #modify number for user options
        #send email if price goes under 100, this number is abitrary for time being
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
    time.sleep(1800)