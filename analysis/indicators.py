def calculate_ma(history, days):
    return history["Close"].tail(days).mean()

def calculate_rsi(history, days=14):
    delta = history["Close"].diff()
    gain = delta.where(delta > 0, 0).tail(days).mean()
    loss = -delta.where(delta < 0, 0).tail(days).mean()

    if loss == 0:
        return 100

    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(history):
    ema12 = history["Close"].ewm(span=12, adjust=False).mean()
    ema26 = history["Close"].ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal_line = macd_line.ewm(span=9, adjust=False).mean()

    return macd_line.iloc[-1], signal_line.iloc[-1]
