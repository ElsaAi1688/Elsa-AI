
import json
from pathlib import Path

from manager.decision_manager import DecisionManager
from services.line_service import send_line_message

CACHE = Path("data/ai_cache/market_scan.json")

data = json.loads(CACHE.read_text(encoding="utf-8"))
stocks = data["stocks"]

top10 = stocks[:10]
manager = DecisionManager()

lines = []
lines.append("🧑‍💼 Elsa AI Build 007")
lines.append("今日 AI 經理人決策報告")
lines.append("=" * 30)
lines.append(f"資料時間：{data['updated_at']}")
lines.append("")

for i, stock in enumerate(top10[:5], 1):
    d = manager.decide(stock)

    lines.append(f"{i}. {d['name']} {d['level']}")
    lines.append(f"AI：{d['score']}｜突破率：{d['breakout']}%")
    lines.append(f"現價：{d['price']}｜支撐：{d['support']}｜壓力：{d['resistance']}")
    lines.append(f"經理人建議：{d['action']}")
    lines.append("原因：")
    for r in d["reasons"][:4]:
        lines.append(f"✔ {r}")
    lines.append("-" * 30)

lines.append("📌 今日總結")
lines.append("高分股票不代表立刻買，需等待突破確認、量能配合，並設定停損。")

msg = "\n".join(lines)

Path("reports/build007_manager_report.txt").write_text(msg, encoding="utf-8")

print(msg)
send_line_message(msg)
