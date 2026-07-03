import yfinance as yf

class ChipEngine:

    def analyze(self, symbol):

        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="30d")

        if hist.empty:
            return None

        volume = hist["Volume"].tail(5).mean()
        last_volume = hist["Volume"].iloc[-1]

        score = 50
        reasons = []

        if last_volume > volume * 1.5:
            score += 20
            reasons.append("成交量明顯放大")

        elif last_volume > volume:
            score += 10
            reasons.append("成交量高於平均")

        change = (
            hist["Close"].iloc[-1]
            - hist["Close"].iloc[-5]
        ) / hist["Close"].iloc[-5] * 100

        if change > 5:
            score += 20
            reasons.append("短線動能強")

        elif change > 2:
            score += 10
            reasons.append("短線轉強")

        return {
            "chip_score": min(score,100),
            "avg_volume": int(volume),
            "last_volume": int(last_volume),
            "price_change": round(change,2),
            "reasons": reasons
        }

if __name__=="__main__":

    engine = ChipEngine()

    print(engine.analyze("2324.TW"))
