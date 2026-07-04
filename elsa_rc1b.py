
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

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
