
from core.elsa_brain import ElsaBrain
from services.line_service import send_line_message

brain = ElsaBrain().update(limit=200)

lines = []
lines.append("🧠 Elsa Core Brain 已更新")
lines.append("=" * 30)
lines.append(f"更新時間：{brain['updated_at']}")
lines.append(f"市場分數：{brain['market']['score']}/100")
lines.append(f"掃描股票數：{brain['market']['count']}")
lines.append(f"投資健康度：{brain['portfolio_health']['score']}/100｜{brain['portfolio_health']['level']}")
lines.append("")
lines.append("🔥 今日 Top3")
for i, s in enumerate(brain["market"]["top10"][:3], 1):
    lines.append(f"{i}. {s['name']} AI {s['ai_score']}")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
