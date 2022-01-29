#Data Source
import yfinance as yf

#Interval required 1 minute
data = yf.download(tickers='UBER', period='1d', interval='1m')

print(data)