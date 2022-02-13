
from flask import Flask, request, render_template, jsonify
import yfinance as yf

app = Flask(__name__)

#quote price
@app.route("/quote")
def display_quote():
	symbol = request.args.get('symbol', default="AAPL")
	quote = yf.Ticker(symbol)
	return jsonify(quote.info)

#Pull history
@app.route("/history")
def display_history():
	symbol = request.args.get('symbol', default="NVDA")
	period = request.args.get('period', default="1y")
	interval = request.args.get('interval', default="1mo")
	quote = yf.Ticker(symbol)	
	hist = quote.history(period=period, interval=interval)
	data = hist.to_json()
	return data

#route back to homepage
@app.route("/")
def home():
    return render_template("base.html")
if __name__ == "__main__":
	app.run(debug=True)
