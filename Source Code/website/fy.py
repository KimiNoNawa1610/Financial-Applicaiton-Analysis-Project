import yfinance as fy

def getStockPrice1d(stock):
    print(stock)
    info = fy.Ticker(str(stock).strip())
    todaydata=info.history(period="1d")
    return round(todaydata["Close"][0],3)

def getCurrentPrice(stock):
    stock = fy.Ticker(str(stock).strip())
    price= stock.info['regularMarketPrice']
    return price

