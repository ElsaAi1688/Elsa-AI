
import json
from pathlib import Path

from manager.decision_manager import DecisionManager
from manager.decision_journal import DecisionJournal
from services.line_service import send_line_message

CACHE = Path("data/ai_cache/market_scan.json")

data = json.loads(CACHE.read_text(encoding="utf-8"))
stocks = data["stocks"]

manager = DecisionManager()
journal = DecisionJournal()

lines = []
lines.append("📖 Elsa AI Build 008")
lines.append("AI 決策日誌已更新")
lines.append("=" * 30)

for stock in stocks[:5]:
    decision = manager.decide(stock)
    item = journal.record(decision)

    lines.append(f"{item['name']}｜AI {item['ai_score']}｜{item['level']}")
    lines.append(f"建議：{item['action']}")
    lines.append("-" * 30)

lines.append("之後 Elsa 會追蹤這些建議，檢查一週後、兩週後結果。")

msg = "\n".join(lines)

Path("reports/build008_journal_report.txt").write_text(msg, encoding="utf-8")

print(msg)
send_line_message(msg)
