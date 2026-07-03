import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from data_provider import DataProvider


class TechnicalEngine:

    def analyze_from_data(self, df):

        if df.empty:
            return None

        df = df.copy()

        df["MA5"] = df["Close"].rolling(5).mean()
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA60"] = df["Close"].rolling(60).mean()

        latest = df.iloc[-1]

        score = 50
        reasons = []

        close = float(latest["Close"])

        if close > float(latest["MA5"]):
            score += 5
            reasons.append("站上 MA5")

        if close > float(latest["MA20"]):
            score += 10
            reasons.append("站上 MA20")

        if close > float(latest["MA60"]):
            score += 15
            reasons.append("站上 MA60")

        return {
            "price": round(close, 2),
            "technical_score": min(score, 100),
            "reasons": reasons
        }

    def analyze(self, symbol):

        df = DataProvider().get_history(symbol)

        return self.analyze_from_data(df)


if __name__ == "__main__":
    print(TechnicalEngine().analyze("2324.TW"))
