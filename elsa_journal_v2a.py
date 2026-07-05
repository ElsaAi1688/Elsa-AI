from workspace.workspace_engine import WorkspaceEngine
from memory.investment_journal import InvestmentJournal
from services.line_service import send_line_message

data = WorkspaceEngine().build()
item = InvestmentJournal().record_daily(data)

lines = []
lines.append("📝 Elsa Investment Journal v2-A")
lines.append("=" * 30)
lines.append(f"日期：{item['date']} {item['time']}")
lines.append(f"今日總決策：{item['main_decision']}")
lines.append(f"投資健康度：{item['portfolio_health']}/100｜{item['portfolio_level']}")
lines.append("")
lines.append("📈 今日持股決策")
for h in item["holdings"]:
    lines.append(f"{h['name']}｜{h['action']}｜信心 {h['confidence']}%")
lines.append("")
lines.append("📚 今日老師")
lines.append(item["lesson"])

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
