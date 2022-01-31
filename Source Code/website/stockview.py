#Data Source
import yfinance as yf

#Interval required 1 minute

def getData(name):
    data = yf.download(tickers=name, period='1d', interval='1m')
    return data