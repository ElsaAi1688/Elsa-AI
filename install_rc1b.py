from pathlib import Path

Path("portfolio/portfolio_health.py").write_text('''
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
''', encoding="utf-8")

Path("elsa_rc1b.py").write_text('''
from portfolio.portfolio_center import PortfolioCenter
from portfolio.portfolio_health import PortfolioHealth
from services.line_service import send_line_message

portfolio = PortfolioCenter().analyze()
health = PortfolioHealth().calculate(portfolio)

lines = []
lines.append("📊 Elsa AI RC1-B 投資健康度")
lines.append("=" * 30)
lines.append(f"健康度：{health['score']}/100｜{health['level']}")
lines.append(f"評等：{health['stars']}")
lines.append("")
lines.append(f"投入成本：{portfolio['total_cost']}")
lines.append(f"目前市值：{portfolio['total_value']}")
lines.append(f"未實現損益：{portfolio['total_pnl']}（{portfolio['total_pnl_pct']}%）")
lines.append(f"長期定投比例：{portfolio['dca_ratio']}%")
lines.append(f"短線操作比例：{portfolio['short_ratio']}%")
lines.append("")
lines.append("健康度原因：")
for r in health["reasons"]:
    lines.append(f"✔ {r}")

lines.append("")
lines.append("📌 經理人結論")
if health["score"] >= 75:
    lines.append("目前投資組合結構穩健，可以依照原策略持續執行。")
elif health["score"] >= 60:
    lines.append("目前投資組合尚可，短線部位需持續觀察。")
else:
    lines.append("目前投資組合風險偏高，建議降低短線部位或保留現金。")

msg = "\\n".join(lines)
print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ RC1-B Portfolio Health 安裝完成")
