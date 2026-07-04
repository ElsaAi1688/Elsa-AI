
class DecisionManager:

    def decide(self, stock):
        score = stock["ai_score"]
        breakout = stock["breakout_probability"]
        price = stock["price"]
        resistance = stock["resistance"]
        support = stock["support"]

        if score >= 80 and breakout >= 75:
            action = "可列入今日重點觀察，等待帶量突破再分批布局"
            level = "★★★★★"
        elif score >= 70:
            action = "續抱 / 觀察，不追高"
            level = "★★★★"
        elif score >= 60:
            action = "中性觀察，等待更明確訊號"
            level = "★★★"
        else:
            action = "暫不進場，風險偏高"
            level = "★★"

        reasons = []

        if resistance and price:
            distance = round((resistance - price) / price * 100, 2)
            if distance <= 1:
                reasons.append("距離壓力區很近，不適合盲目追高")
            elif distance <= 3:
                reasons.append("接近壓力區，需觀察是否帶量突破")

        if support and price:
            down_risk = round((price - support) / price * 100, 2)
            reasons.append(f"距離支撐約 {down_risk}%")

        for r in stock.get("reasons", [])[:3]:
            reasons.append(r)

        return {
            "name": stock["name"],
            "symbol": stock["symbol"],
            "score": score,
            "level": level,
            "action": action,
            "price": price,
            "support": support,
            "resistance": resistance,
            "breakout": breakout,
            "reasons": reasons[:6]
        }
