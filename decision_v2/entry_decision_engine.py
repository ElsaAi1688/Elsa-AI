class EntryDecisionEngine:

    def evaluate(self, data):
        price = data["price"]
        support = data["support"]
        resistance = data["resistance"]
        technical_score = data["technical_score"]
        fundamental_score = data["fundamental_score"]
        chip_score = data["chip_score"]

        score = round(
            technical_score * 0.5 +
            fundamental_score * 0.25 +
            chip_score * 0.25
        )

        reasons = []

        if technical_score >= 75:
            reasons.append("技術面偏強")
        elif technical_score < 60:
            reasons.append("技術面尚未成熟")

        if fundamental_score >= 65:
            reasons.append("基本面尚可")
        elif fundamental_score < 50:
            reasons.append("基本面偏弱")

        if chip_score >= 65:
            reasons.append("法人籌碼偏多")
        elif chip_score < 50:
            reasons.append("法人籌碼偏弱")

        if resistance and price >= resistance * 0.98:
            score -= 10
            reasons.append("接近壓力，不適合追高")

        if support and price <= support * 1.02:
            score += 8
            reasons.append("接近短線支撐，風險報酬較佳")

        score = max(0, min(100, score))

        entry_low = round(support, 2)
        entry_high = round(min(price, support * 1.02), 2)
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
