from datetime import datetime
import json
from pathlib import Path
from services.line_service import send_line_message

today = datetime.now().strftime("%Y-%m-%d")
log_file = Path("data/decision_log.json")

lines = []
lines.append("🌅 Elsa AI Morning Brief v2.1")
lines.append("=" * 30)
lines.append(f"日期：{today}")
lines.append("")

today_data = []

if log_file.exists():
    data = json.loads(log_file.read_text(encoding="utf-8"))
    today_data = [x for x in data if x.get("date") == today]
    today_data = sorted(today_data, key=lambda x: x.get("score", 0), reverse=True)

lines.append("📈 今日操作策略")
lines.append("-" * 30)

if not today_data:
    lines.append("今天尚未產生決策資料，請先執行 multi_report.py")
else:
    for stock in today_data:
        symbol = stock.get("symbol", "")
        name = stock.get("name", "")
        score = stock.get("score", 0)
        confidence = stock.get("confidence", 0)
        risk = stock.get("risk_level", "未評估")
        suggestion = stock.get("suggestion", stock.get("recommendation", "觀察"))

        lines.append(f"{symbol} {name}")
        lines.append(f"AI分數：{score}/100")
        lines.append(f"信心值：{confidence}/100")
        lines.append(f"風險：{risk}")
        lines.append(f"建議：{suggestion}")
        lines.append("")

lines.append("⭐ 今日最高分")
lines.append("-" * 30)

if today_data:
    best = today_data[0]
    lines.append(f"{best.get('symbol')} {best.get('name')}")
    lines.append(f"AI分數：{best.get('score')}/100")
    lines.append(f"建議：{best.get('suggestion', '觀察')}")
else:
    lines.append("尚無資料")

lines.append("")
lines.append("📚 今日股票教室")
lines.append("-" * 30)
lines.append("今天重點：先看 AI 分數，再看風險等級。")
lines.append("高分不代表一定買，還要確認是否符合妳的策略。")
lines.append("")
lines.append("📰 新聞分析：下一階段加入")
lines.append("👥 籌碼分析：下一階段加入")
lines.append("=" * 30)

report = "\n".join(lines)

print(report)
send_line_message(report)
