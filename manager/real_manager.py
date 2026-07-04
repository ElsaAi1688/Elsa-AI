
class RealManager:

    def analyze(self, stock):
        price = stock["price"]
        support = stock["support"]
        resistance = stock["resistance"]
        stop_loss = stock["stop_loss"]
        target = stock["target_price"]
        score = stock["ai_score"]
        breakout = stock["breakout_probability"]

        risk_pct = 0
        reward_pct = 0
        rr = 0

        if price and stop_loss and price > stop_loss:
            risk_pct = round((price - stop_loss) / price * 100, 2)

        if price and target and target > price:
            reward_pct = round((target - price) / price * 100, 2)

        if risk_pct > 0:
            rr = round(reward_pct / risk_pct, 2)

        confidence = min(95, max(30, int(
            score * 0.55 +
            breakout * 0.25 +
            stock["technical_score"] * 0.10 +
            stock["chip_score"] * 0.10
        )))

        if score >= 80 and breakout >= 75 and rr >= 2:
            action = "可列入重點進場觀察，等待帶量突破後分批布局"
            tone = "偏積極"
        elif score >= 70 and rr >= 1.5:
            action = "續抱觀察，不建議追高，等待更好買點"
            tone = "穩健"
        elif score >= 60:
            action = "中性觀察，暫時不要急著進場"
            tone = "保守"
        else:
            action = "暫不進場，先避開風險"
            tone = "防守"

        buy_zone_1 = round(support * 1.01, 2) if support else 0
        buy_zone_2 = round(support * 0.99, 2) if support else 0
        add_zone = round(resistance * 1.01, 2) if resistance else 0
        take_profit_1 = target
        take_profit_2 = round(target * 1.04, 2) if target else 0

        manager_text = []

        manager_text.append(f"今天操作風格：{tone}")
        manager_text.append(action)

        if resistance and price:
            distance_to_resistance = round((resistance - price) / price * 100, 2)
            if distance_to_resistance <= 1:
                manager_text.append("目前距離壓力區很近，不適合盲目追高。")
            elif distance_to_resistance <= 3:
                manager_text.append("股價接近壓力區，適合等突破確認。")

        if rr < 1:
            manager_text.append("目前風險報酬比不漂亮，建議等待更好的價格。")
        elif rr >= 2:
            manager_text.append("風險報酬比尚可，若量能配合可以列入觀察。")

        return {
            "name": stock["name"],
            "symbol": stock["symbol"],
            "score": score,
            "confidence": confidence,
            "tone": tone,
            "action": action,
            "price": price,
            "support": support,
            "resistance": resistance,
            "stop_loss": stop_loss,
            "target": target,
            "risk_pct": risk_pct,
            "reward_pct": reward_pct,
            "rr": rr,
            "buy_zone_1": buy_zone_1,
            "buy_zone_2": buy_zone_2,
            "add_zone": add_zone,
            "take_profit_1": take_profit_1,
            "take_profit_2": take_profit_2,
            "manager_text": manager_text,
            "reasons": stock.get("reasons", [])[:5],
        }
