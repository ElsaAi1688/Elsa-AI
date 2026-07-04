
class PortfolioHealth:

    def calculate(self, portfolio):
        avg_ai = portfolio["avg_ai"]
        dca_ratio = portfolio["dca_ratio"]
        short_ratio = portfolio["short_ratio"]
        pnl_pct = portfolio["total_pnl_pct"]

        score = 50
        reasons = []

        if avg_ai >= 75:
            score += 25
            reasons.append("持股平均 AI 分數良好")
        elif avg_ai >= 60:
            score += 15
            reasons.append("持股 AI 分數穩健")
        else:
            score -= 10
            reasons.append("持股 AI 分數偏弱")

        if dca_ratio >= 50:
            score += 15
            reasons.append("長期定投比例健康")
        elif dca_ratio >= 30:
            score += 8
            reasons.append("長期配置尚可")

        if short_ratio > 40:
            score -= 12
            reasons.append("短線部位偏高，風險較大")
        else:
            score += 8
            reasons.append("短線部位控制合理")

        if pnl_pct >= 5:
            score += 10
            reasons.append("目前整體投資組合有獲利")
        elif pnl_pct < -5:
            score -= 10
            reasons.append("目前整體損益偏弱，需控管風險")

        score = max(0, min(100, round(score)))

        if score >= 85:
            level = "優秀"
            stars = "★★★★★"
        elif score >= 70:
            level = "穩健"
            stars = "★★★★"
        elif score >= 55:
            level = "普通"
            stars = "★★★"
        else:
            level = "偏弱"
            stars = "★★"

        return {
            "score": score,
            "level": level,
            "stars": stars,
            "reasons": reasons
        }
