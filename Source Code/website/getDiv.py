from sklearn.preprocessing import SplineTransformer
import yfinance as yf
import math, time, requests, lxml
from lxml import html
import random
import smtplib
import pandas


def getStockPrice(stock):
    print(stock)
    info = yf.Ticker(str(stock).strip())
    todaydata=info.history(period="1d")
    return round(todaydata["Close"][0],3)

def formatdate(date_datetime):
     date_timetuple = date_datetime.timetuple()
     date_mktime = time.mktime(date_timetuple)
     date_int = int(date_mktime)
     date_str = str(date_int)
     return date_str

#FOR TABLE DISPLAY (DIRECTLY FROM DOCUMENTATION)
def subdomain(symbol, start, end):
     format_url = "{0}/history?period1={1}&period2={2}"    
     tail_url = "&interval=div%7Csplit&filter=div&frequency=1d"
     subdomain = format_url.format(symbol, start, end) + tail_url
     return subdomain

def scrape_page(url, header):
     page = requests.get(url, headers=header)
     element_html = html.fromstring(page.content)
     table = element_html.xpath('//table')
     table_tree = lxml.etree.tostring(table[0], method='xml')
     panda = pandas.read_html(table_tree)
     return panda

def clean_dividends(symbol, dividends):
     index = len(dividends)     
     dividends = dividends.drop(index-1)
     dividends = dividends.set_index('Date')
     dividends = dividends['Dividends']
     dividends = dividends.str.replace(r'\Dividend', '')
     dividends = dividends.astype(float)
     dividends.name = symbol
     return dividends
#END


class getDiv(yf.Ticker):
    x = yf.Ticker.dividents
    price = x + getStockPrice(yf.Ticker)
    #100 + divident return per stock
    x.actions
    div = x.dividends
    split = x.splits
    
