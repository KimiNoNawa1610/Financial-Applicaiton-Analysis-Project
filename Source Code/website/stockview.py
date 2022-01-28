import plotly.graph_objs as go
import yfinance as yf

data = yf.download(tickers=stock_price, period = ‘how_many_days’, interval = ‘how_long_between_each_check’, rounding= bool)
data = yf.download(tickers='GOOG', period = '5d', interval = '15m', rounding= True)
print(data)