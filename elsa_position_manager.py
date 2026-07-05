from portfolio.portfolio_center import PortfolioCenter
from position.position_manager import PositionManager
from services.line_service import send_line_message

pm=PositionManager()

portfolio=PortfolioCenter().analyze()

rows=[]

for h in portfolio["holdings"]:

    s=pm.score(h)

    rows.append((s,h))

rows.sort(reverse=True,key=lambda x:x[0])

lines=[]

lines.append("👩‍💼 Elsa Position Manager")
lines.append("="*30)

for score,h in rows:

    watch="🔥需要盯盤" if score>=60 else "✅正常"

    lines.append(f"{h['name']}")
    lines.append(f"重要度：{score}/100")
    lines.append(watch)
    lines.append("")

lines.append("")

lines.append("⭐ 今天請優先管理第一名持股")

lines.append(rows[0][1]["name"])

msg="\n".join(lines)

print(msg)

send_line_message(msg)
