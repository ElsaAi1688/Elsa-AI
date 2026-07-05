class ConfidenceEngine:

    def explain(self, stock, action):
        score = 50
        reasons = []

        ai = stock["ai_score"]
        breakout = stock["breakout_probability"]
        strategy = stock.get("strategy", "")
        pnl_pct = stock.get("pnl_pct", 0)

        if ai >= 75:
            score += 18
            reasons.append("AI 分數偏強")
        elif ai >= 60:
            score += 8
            reasons.append("AI 分數穩健")
        else:
            score -= 12
            reasons.append("AI 分數偏弱")

        if breakout >= 75:
            score += 15
            reasons.append("突破率高")
        elif breakout >= 60:
            score += 8
            reasons.append("突破率中等")
        else:
            score -= 8
            reasons.append("突破率不足")

        if strategy == "long_term_dca":
            score += 10
            reasons.append("屬於長期定投，短線波動影響較小")

        if strategy == "short_term":
            if pnl_pct < -3:
                score -= 10
                reasons.append("短線目前虧損，需保守")
            else:
                score += 5
                reasons.append("短線風險尚可控")

        if action == "等待":
            score += 10
            reasons.append("等待可以降低追高風險")

        score = max(0, min(100, round(score)))

        return {
            "confidence": score,
            "confidence_reasons": reasons
        }
