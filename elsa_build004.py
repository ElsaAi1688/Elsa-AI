
from scanner.market_cache import save_market_scan, load_market_scan
from services.line_service import send_line_message

save_market_scan(limit=200)

cache = load_market_scan()
stocks = cache["stocks"]

top10 = stocks[:10]
elite = [s for s in stocks if s["ai_score"] >= 75][:3]
watch = [s for s in stocks if 60 <= s["ai_score"] < 75][:8]
avoid = [s for s in stocks if s["ai_score"] < 55][:5]

lines = []
lines.append("🧠 Elsa AI Build 004")
lines.append("AI Database + Market Cache")
lines.append("=" * 30)
lines.append(f"更新時間：{cache['updated_at']}")
lines.append(f"掃描股票數：{cache['count']}")
lines.append("")

lines.append("🔥 今日 Top10")
for i, s in enumerate(top10, 1):
    lines.append(f"{i}. {s['name']} AI {s['ai_score']} 現價 {s['price']}")

lines.append("")
lines.append("🏆 Elite")
if elite:
    for s in elite:
        lines.append(f"{s['name']} AI {s['ai_score']} 突破率 {s['breakout_probability']}%")
else:
    lines.append("今日暫無 Elite")

lines.append("")
lines.append("⭐ Watch List")
for s in watch:
    lines.append(f"{s['name']} AI {s['ai_score']} 突破率 {s['breakout_probability']}%")

lines.append("")
lines.append("🚫 Avoid")
if avoid:
    for s in avoid:
        lines.append(f"{s['name']} AI {s['ai_score']}")
else:
    lines.append("今日暫無明顯 Avoid")

msg = "\n".join(lines)

print(msg)
send_line_message(msg)
