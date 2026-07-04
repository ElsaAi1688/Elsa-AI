from core.elsa_brain import ElsaBrain
from services.line_service import send_line_message

brain = ElsaBrain().load()

if brain is None:
    brain = ElsaBrain().update(limit=200)

market = brain["market"]
portfolio = brain["portfolio"]

lines = []
lines.append("🌇 Elsa AI 收盤分析 Core")
lines.append("=" * 30)
lines.append(f"更新時間：{brain['updated_at']}")
lines.append("")

lines.append("📈 今日持股收盤狀態")
for h in portfolio["holdings"]:
    lines.append(f"{h['name']}｜AI {h['ai_score']}｜損益 {h['pnl_pct']}%")
    lines.append(f"建議：{h['manager_advice']}")
lines.append("")

lines.append("🔥 今日強勢 Top5")
for i, s in enumerate(market["top10"][:5], 1):
    lines.append(f"{i}. {s['name']} AI {s['ai_score']}｜突破率 {s['breakout_probability']}%")
lines.append("")

lines.append("⭐ 明日 Watch List")
for s in market["watch"][:5]:
    lines.append(f"{s['name']}｜AI {s['ai_score']}｜突破率 {s['breakout_probability']}%")
lines.append("")

lines.append("📌 明日策略")
lines.append("明天先看 Watch List 是否帶量突破；持股以支撐、壓力、停損為準。")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
