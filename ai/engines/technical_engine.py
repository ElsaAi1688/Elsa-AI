import yfinance as yf
import pandas as pd

class TechnicalEngine:

    def analyze(self, symbol):

        ticker = yf.Ticker(symbol)

        df = ticker.history(period="6mo")

        if df.empty:
            return None

        df["MA5"] = df["Close"].rolling(5).mean()
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA60"] = df["Close"].rolling(60).mean()

        latest = df.iloc[-1]

        score = 50
        reasons = []

        if latest["Close"] > latest["MA5"]:
            score += 5
            reasons.append("站上 MA5")

        if latest["Close"] > latest["MA20"]:
            score += 10
            reasons.append("站上 MA20")

        if latest["Close"] > latest["MA60"]:
            score += 15
            reasons.append("站上 MA60")

        return {
            "price": round(latest["Close"],2),
            "technical_score": score,
            "reasons": reasons
        }

if __name__ == "__main__":

    engine = TechnicalEngine()

    result = engine.analyze("2324.TW")

    print(result)
