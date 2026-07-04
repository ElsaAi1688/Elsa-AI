from core.elsa_brain import ElsaBrain
from services.line_service import send_line_message

brain = ElsaBrain().load()

if brain is None:
    brain = ElsaBrain().update(limit=200)

portfolio = brain["portfolio"]
health = brain["portfolio_health"]
market = brain["market"]

lines = []
lines.append("🌅 Elsa AI Morning Brief Core")
lines.append("=" * 30)
lines.append(f"更新時間：{brain['updated_at']}")
lines.append("")

lines.append("👩 莎莎投資中心")
lines.append(f"投入成本：{portfolio['total_cost']}")
lines.append(f"目前市值：{portfolio['total_value']}")
lines.append(f"未實現損益：{portfolio['total_pnl']}（{portfolio['total_pnl_pct']}%）")
lines.append(f"健康度：{health['score']}/100｜{health['level']} {health['stars']}")
lines.append("")

lines.append("📈 我的持股")
for h in portfolio["holdings"]:
    lines.append(f"{h['name']}｜AI {h['ai_score']}｜損益 {h['pnl_pct']}%")
    lines.append(f"經理人：{h['manager_advice']}")
lines.append("")

lines.append("🔥 今日 Top5")
for i, s in enumerate(market["top10"][:5], 1):
    lines.append(f"{i}. {s['name']} AI {s['ai_score']} 現價 {s['price']}")

lines.append("")
lines.append("🏆 Elite")
if market["elite"]:
    for s in market["elite"]:
        lines.append(f"{s['name']} AI {s['ai_score']}")
else:
    lines.append("今日暫無 Elite")

lines.append("")
lines.append("📌 今日策略")
lines.append("以持股健康度為主，不追高，等待突破與量能確認。")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
