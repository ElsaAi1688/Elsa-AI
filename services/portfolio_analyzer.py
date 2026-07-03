from services.stock_service import get_stock_data
from analysis.indicators import calculate_ma, calculate_rsi, calculate_macd
from analysis.ai_score import analyze


def analyze_stock(stock):
    symbol = stock["symbol"]
    name = stock["name"]
    stock_type = stock.get("strategy", stock.get("type", "watch"))
    buy_price = stock.get("buy_price", 0)
    shares = stock.get("shares", 0)

    history = get_stock_data(symbol)

    if history is None:
        return {
            "symbol": symbol,
            "name": name,
            "error": "找不到股票資料"
        }

    latest = history.iloc[-1]

    close = latest["Close"]
    volume = latest["Volume"]

    ma5 = calculate_ma(history, 5)
    ma20 = calculate_ma(history, 20)
    rsi = calculate_rsi(history)
    macd, signal = calculate_macd(history)

    score, messages, confidence, risk_level = analyze(close, buy_price if buy_price > 0 else close, ma5, ma20, rsi, macd, signal, volume)

    profit = 0
    percent = 0

    if buy_price > 0 and shares > 0:
        profit = (close - buy_price) * shares
        percent = ((close - buy_price) / buy_price) * 100

    return {
        "symbol": symbol,
        "name": name,
        "type": stock_type,
        "close": close,
        "volume": volume,
        "ma5": ma5,
        "ma20": ma20,
        "rsi": rsi,
        "macd": macd,
        "signal": signal,
        "score": score,
        "messages": messages,
        "buy_price": buy_price,
        "shares": shares,
        "profit": profit,
        "percent": percent,
        "confidence": confidence,
        "risk_level": risk_level
    }
