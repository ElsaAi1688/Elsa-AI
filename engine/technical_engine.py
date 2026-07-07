class TechnicalEngine:

    def add(self, explain, name, status, points, reason):
        explain.append({
            "name": name,
            "status": status,
            "points": points,
            "reason": reason
        })

    def analyze(self, df):
        score = 50
        explain = []
        reasons = []

        close = df["close"]
        high = df["max"]
        low = df["min"]
        volume = df["Trading_Volume"]

        price = float(close.iloc[-1])

        ma5 = float(close.rolling(5).mean().iloc[-1])
        ma20 = float(close.rolling(20).mean().iloc[-1])
        ma60 = float(close.rolling(60).mean().iloc[-1])

        if price > ma20:
            score += 10
            self.add(explain, "MA", "偏多", 10, "股價站上 MA20")
            reasons.append("股價站上 MA20")
        else:
            score -= 10
            self.add(explain, "MA", "偏弱", -10, "股價跌破 MA20")

        if ma5 > ma20:
            score += 8
            self.add(explain, "MA", "短線轉強", 8, "MA5 高於 MA20")
            reasons.append("MA5 高於 MA20")

        low9 = low.rolling(9).min()
        high9 = high.rolling(9).max()
        rsv = (close - low9) / (high9 - low9) * 100
        k = rsv.ewm(com=2).mean()
        d = k.ewm(com=2).mean()

        k_now = float(k.iloc[-1])
        d_now = float(d.iloc[-1])
        k_prev = float(k.iloc[-2])
        d_prev = float(d.iloc[-2])

        if k_prev < d_prev and k_now > d_now:
            score += 15
            self.add(explain, "KD", "黃金交叉", 15, "KD 由弱轉強")
            reasons.append("KD 黃金交叉")
        elif k_prev > d_prev and k_now < d_now:
            score -= 15
            self.add(explain, "KD", "死亡交叉", -15, "KD 轉弱")
        else:
            self.add(explain, "KD", "中性", 0, "KD 尚未明確轉強")

        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        hist = macd - signal

        macd_now = float(macd.iloc[-1])
        signal_now = float(signal.iloc[-1])
        hist_now = float(hist.iloc[-1])
        hist_prev = float(hist.iloc[-2])

        if macd_now > signal_now and hist_now > 0:
            score += 15
            self.add(explain, "MACD", "翻紅", 15, "MACD 多方訊號成立")
            reasons.append("MACD 翻紅")
        elif macd_now < signal_now and hist_now < 0:
            score -= 15
            self.add(explain, "MACD", "翻黑", -15, "MACD 空方訊號")
        else:
            self.add(explain, "MACD", "中性", 0, "MACD 尚未明確表態")

        if hist_now > hist_prev:
            score += 6
            self.add(explain, "MACD", "動能增加", 6, "MACD 柱體增加")
        else:
            score -= 5
            self.add(explain, "MACD", "動能縮小", -5, "MACD 柱體縮小")

        mid = close.rolling(20).mean()
        std = close.rolling(20).std()
        boll_upper = float((mid + 2 * std).iloc[-1])
        boll_middle = float(mid.iloc[-1])
        boll_lower = float((mid - 2 * std).iloc[-1])

        if price <= boll_lower * 1.02:
            score += 10
            self.add(explain, "BOLL", "接近下軌", 10, "股價接近布林下軌，風險報酬較佳")
        elif price >= boll_upper * 0.98:
            score -= 10
            self.add(explain, "BOLL", "接近上軌", -10, "股價接近布林上軌，不追高")
        else:
            self.add(explain, "BOLL", "區間內", 0, "股價仍在布林通道中")

        vol_now = float(volume.iloc[-1])
        vol_avg = float(volume.tail(20).mean())

        if vol_now > vol_avg * 1.2 and price > float(close.iloc[-2]):
            score += 12
            self.add(explain, "Volume", "量增價漲", 12, "成交量放大且股價上漲")
            reasons.append("量增價漲")
        elif vol_now > vol_avg * 1.5 and price < float(close.iloc[-2]):
            score -= 18
            self.add(explain, "Volume", "爆量下跌", -18, "爆量下跌風險")
        else:
            self.add(explain, "Volume", "量能普通", 0, "量能尚未明顯表態")

        return {
            "score": max(0, min(round(score), 100)),
            "price": round(price, 2),
            "ma5": round(ma5, 2),
            "ma20": round(ma20, 2),
            "ma60": round(ma60, 2),
            "k": round(k_now, 2),
            "d": round(d_now, 2),
            "macd": round(macd_now, 4),
            "macd_signal": round(signal_now, 4),
            "macd_hist": round(hist_now, 4),
            "boll_upper": round(boll_upper, 2),
            "boll_middle": round(boll_middle, 2),
            "boll_lower": round(boll_lower, 2),
            "volume": round(vol_now),
            "avg_volume": round(vol_avg),
            "reasons": reasons,
            "explain": explain
        }
