import yfinance as yf

class FundamentalEngine:

    def analyze(self, symbol):

        ticker = yf.Ticker(symbol)
        info = ticker.info

        score = 50
        reasons = []

        pe = info.get("trailingPE")
        roe = info.get("returnOnEquity")
        market_cap = info.get("marketCap")
        dividend = info.get("dividendYield")

        if pe:
            if pe < 15:
                score += 15
                reasons.append("本益比偏低")
            elif pe < 25:
                score += 8
                reasons.append("本益比合理")

        if roe:
            roe = roe * 100
            if roe > 15:
                score += 15
                reasons.append("ROE 優秀")
            elif roe > 10:
                score += 8
                reasons.append("ROE 良好")

        if dividend:
            dividend = dividend * 100
            if dividend > 5:
                score += 10
                reasons.append("殖利率佳")

        return {
            "fundamental_score": min(score,100),
            "pe": pe,
            "roe": roe,
            "market_cap": market_cap,
            "dividend": dividend,
            "reasons": reasons
        }

if __name__=="__main__":

    engine = FundamentalEngine()

    result = engine.analyze("2324.TW")

    print(result)
