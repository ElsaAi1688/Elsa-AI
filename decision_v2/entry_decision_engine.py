class EntryDecisionEngine:

    def evaluate(self, data):
        price = data["price"]
        support = data["support"]
        resistance = data["resistance"]
        ai = data["ai"]
        breakout = data["breakout"]
        ma5 = data["ma5"]
        ma20 = data["ma20"]
        volume = data["volume"]
        avg_volume = data["avg_volume"]

        score = 50
        reasons = []

        if price > ma20:
            score += 10
            reasons.append("股價站上月線，短線結構尚可")
        else:
            score -= 10
            reasons.append("股價仍在月線下方，需保守")

        if ma5 > ma20:
            score += 10
            reasons.append("MA5 高於 MA20，短線偏多")
        else:
            score -= 5
            reasons.append("MA5 尚未站上 MA20")

        if volume > avg_volume * 1.2:
            score += 10
            reasons.append("成交量放大，有資金進場跡象")
        else:
            reasons.append("成交量尚未明顯放大")

        if price <= support * 1.03:
            score += 12
            reasons.append("股價接近支撐，風險報酬較佳")
        elif price >= resistance * 0.98:
            score -= 12
            reasons.append("股價接近壓力，不適合追高")

        if ai >= 75:
            score += 10
            reasons.append("AI 分數偏強")
        elif ai < 60:
            score -= 10
            reasons.append("AI 分數不足")

        if breakout >= 75:
            score += 10
            reasons.append("突破率偏高")
        elif breakout < 60:
            score -= 5
            reasons.append("突破率尚未成熟")

        score = max(0, min(100, round(score)))

        entry_low = round(max(support, price * 0.985), 2)
        entry_high = round(price, 2)
        stop_loss = round(support * 0.97, 2)
        target1 = round(price * 1.05, 2)
        target2 = round(price * 1.10, 2)

        if score >= 80:
            action = "可第一筆布局"
            level = "★★★★☆"
        elif score >= 68:
            action = "可觀察，等拉回或確認"
            level = "★★★☆☆"
        else:
            action = "等待，不進場"
            level = "★★☆☆☆"

        return {
            "score": score,
            "action": action,
            "level": level,
            "entry_low": entry_low,
            "entry_high": entry_high,
            "stop_loss": stop_loss,
            "target1": target1,
            "target2": target2,
            "reasons": reasons
        }
