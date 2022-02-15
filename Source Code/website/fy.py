import yfinance as fy

def getStockPrice(stock):
    info = fy.Ticker(str(stock).strip())
    todaydata=info.history(period="1d")
    print(todaydata)
    return round(todaydata["Close"][0],3)
