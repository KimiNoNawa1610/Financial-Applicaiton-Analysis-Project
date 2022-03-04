from sklearn.preprocessing import SplineTransformer
import yfinance as yf
import math
import random
import smtplib

def getStockPrice(stock):
    print(stock)
    info = yf.Ticker(str(stock).strip())
    todaydata=info.history(period="1d")
    return round(todaydata["Close"][0],3)

class getDiv(ticker):
    x = ticker.dividents
    price = x + getStockPrice(ticker)
    #100 + divident return per stock
    x.actions
    div = x.dividends
    split = x.splits
    
