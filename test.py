import yfinance as yf

tickers = yf.Tickers('msft aapl goog')
# ^ returns a named tuple of Ticker objects

# access each ticker using (example)
# print(tickers.tickers['AAPL'].history(period="50d")['Close'].mean())
print(tickers.tickers['AAPL'].history()['Close'][-1])
