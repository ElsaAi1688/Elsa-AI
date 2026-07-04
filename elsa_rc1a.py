
from portfolio.portfolio_center import PortfolioCenter
from services.line_service import send_line_message

p = PortfolioCenter().analyze()

lines = []
lines.append("👩 莎莎投資中心 RC1-A 正式版")
lines.append("=" * 30)
lines.append(f"投入成本：{p['total_cost']}")
lines.append(f"目前市值：{p['total_value']}")
lines.append(f"未實現損益：{p['total_pnl']}（{p['total_pnl_pct']}%）")
lines.append(f"投資健康度：{p['avg_ai']}/100｜{p['health']}")
lines.append(f"長期定投比例：{p['dca_ratio']}%")
lines.append(f"短線操作比例：{p['short_ratio']}%")
lines.append("")

for h in p["holdings"]:
    lines.append(f"📈 {h['name']}（{h['symbol']}）")
    lines.append(f"策略：{h['strategy_label']}")
    lines.append(f"成本：{h['cost']}｜現價：{h['price']}｜股數：{h['shares']}")
    lines.append(f"投入：{h['invested']}｜市值：{h['value']}")
    lines.append(f"損益：{h['pnl']}（{h['pnl_pct']}%）")
    lines.append(f"AI：{h['ai_score']}｜建議：{h['recommendation']}")
    lines.append(f"經理人：{h['manager_advice']}")
    lines.append(f"支撐：{h['support']}｜壓力：{h['resistance']}")
    lines.append(f"停損：{h['stop_loss']}｜目標：{h['target_price']}")
    lines.append("-" * 30)

lines.append("📌 經理人一句話")
lines.append(p["manager_summary"])

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
