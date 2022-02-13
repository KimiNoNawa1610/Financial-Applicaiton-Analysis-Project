#Data Source
import yfinance as yf
import pandas as pd
import plotly
import plotly.express as px
import json

#Interval required 1 minute
#Pull history

def getData(name):
    data = yf.download(tickers=name, period='1d', interval='1m')
    return data