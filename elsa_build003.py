import sys
from scanner.market_brain import MarketBrain
from services.line_service import send_line_message

limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100

brain = MarketBrain()
stocks = brain.scan(limit=limit)

lines = []
lines.append(f"🧠 Elsa AI Build 003 Market Brain｜掃描 {limit} 檔")
lines.append("=" * 30)

lines.append("🔥 今日 Top10")
for i, s in enumerate(brain.top10(stocks), 1):
    lines.append(f"{i}. {s.name} AI {s.ai_score} 現價 {s.price}")

lines.append("")
lines.append("🏆 Elite")
elite = brain.elite(stocks)
if elite:
    for s in elite:
        lines.append(f"{s.name} AI {s.ai_score}")
else:
    lines.append("今日暫無 Elite")

lines.append("")
lines.append("⭐ Watch List")
for s in brain.watch(stocks)[:8]:
    lines.append(f"{s.name} AI {s.ai_score} 突破率 {s.breakout_probability}%")

lines.append("")
lines.append("🚫 Avoid")
avoid = brain.avoid(stocks)
if avoid:
    for s in avoid[:5]:
        lines.append(f"{s.name} AI {s.ai_score}")
else:
    lines.append("今日暫無明顯 Avoid")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
