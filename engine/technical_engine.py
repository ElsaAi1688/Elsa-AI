class TechnicalEngine:

    def analyze(self, df):
        score = 50
        reasons = []

        close = df["close"]
        price = float(close.iloc[-1])

        ma5 = float(close.rolling(5).mean().iloc[-1])
        ma10 = float(close.rolling(10).mean().iloc[-1])
        ma20 = float(close.rolling(20).mean().iloc[-1])
        ma60 = float(close.rolling(60).mean().iloc[-1])

        if price > ma5:
            score += 3
            reasons.append("股價站上 MA5")
        if price > ma10:
            score += 4
            reasons.append("股價站上 MA10")
        if price > ma20:
            score += 8
            reasons.append("股價站上 MA20")
        if ma5 > ma20:
            score += 5
            reasons.append("MA5 高於 MA20")
        if ma20 > ma60:
            score += 8
            reasons.append("MA20 高於 MA60")

        if price < ma20:
            score -= 10
            reasons.append("跌破 MA20")
        if price < ma60:
            score -= 15
            reasons.append("跌破 MA60")

        low9 = df["min"].rolling(9).min()
        high9 = df["max"].rolling(9).max()
        rsv = (close - low9) / (high9 - low9) * 100
        k = rsv.ewm(com=2).mean()
        d = k.ewm(com=2).mean()

        k_now = float(k.iloc[-1])
        d_now = float(d.iloc[-1])
        k_prev = float(k.iloc[-2])
        d_prev = float(d.iloc[-2])

        if k_prev < d_prev and k_now > d_now:
            score += 15
            reasons.append("KD 黃金交叉")
        elif k_prev > d_prev and k_now < d_now:
            score -= 15
            reasons.append("KD 死亡交叉")

        if k_now < 20:
            score += 8
            reasons.append("KD 低檔區")
        elif k_now > 80:
            score -= 8
            reasons.append("KD 高檔過熱")

        return {
            "score": max(0, min(round(score), 100)),
            "price": round(price, 2),
            "ma5": round(ma5, 2),
            "ma10": round(ma10, 2),
            "ma20": round(ma20, 2),
            "ma60": round(ma60, 2),
            "k": round(k_now, 2),
            "d": round(d_now, 2),
            "reasons": reasons
        }
