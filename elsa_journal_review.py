import json
from pathlib import Path
from services.line_service import send_line_message

JOURNAL = Path("memory/investment_journal.json")

if not JOURNAL.exists():
    msg = "目前還沒有投資日誌。"
else:
    records = json.loads(JOURNAL.read_text(encoding="utf-8"))
    recent = records[-5:]

    lines = []
    lines.append("📖 Elsa 投資日誌回顧")
    lines.append("=" * 30)

    for r in recent:
        lines.append(f"日期：{r['date']} {r['time']}")
        lines.append(f"總決策：{r['main_decision']}")
        lines.append(f"健康度：{r['portfolio_health']}/100｜{r['portfolio_level']}")
        lines.append("持股決策：")
        for h in r["holdings"]:
            lines.append(f"・{h['name']}｜{h['action']}｜信心 {h['confidence']}%")
        lines.append("-" * 30)

    lines.append("📌 Elsa 回顧")
    lines.append("我會持續記錄每天的決策，之後用來檢查哪些判斷有效、哪些需要修正。")

    msg = "\n".join(lines)

print(msg)
send_line_message(msg)
