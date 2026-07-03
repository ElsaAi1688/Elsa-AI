import yfinance as yf

def get_stock_data(stock_no):
    symbol = stock_no + ".TW"
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="90d")

    if history.empty:
        return None

    return history
