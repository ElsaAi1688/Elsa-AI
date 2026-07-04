from scanner.market_cache import load_market_scan
from services.line_service import send_line_message

cache = load_market_scan()
stocks = cache["stocks"]

top10 = stocks[:10]
turn_strong = [s for s in stocks if s["ai_score"] >= 75][:5]
risk = [s for s in stocks if s["ai_score"] < 55][:5]

lines = []
lines.append("🌇 Elsa AI 收盤分析 2.0")
lines.append("=" * 30)
lines.append(f"資料時間：{cache['updated_at']}")
lines.append("")

lines.append("🔥 今日強勢股")
for i, s in enumerate(top10[:5], 1):
    lines.append(f"{i}. {s['name']} AI {s['ai_score']}｜突破率 {s['breakout_probability']}%")
lines.append("")

lines.append("🏆 今日轉強 Elite")
if turn_strong:
    for s in turn_strong:
        lines.append(f"{s['name']}｜AI {s['ai_score']}｜現價 {s['price']}")
else:
    lines.append("今日暫無明顯轉強股")
lines.append("")

lines.append("🚫 今日風險名單")
if risk:
    for s in risk:
        lines.append(f"{s['name']}｜AI {s['ai_score']}｜暫不追蹤")
else:
    lines.append("今日暫無明顯風險股")
lines.append("")

lines.append("📌 明日策略")
lines.append("明天優先觀察 Elite 與 Watch List，不追高，等突破確認。")

msg = "\n".join(lines)
print(msg)
send_line_message(msg)
