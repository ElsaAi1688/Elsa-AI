from pathlib import Path

Path("data/ai_cache").mkdir(parents=True, exist_ok=True)

Path("scanner/market_cache.py").write_text('''
import json
from pathlib import Path
from datetime import datetime
from scanner.market_brain import MarketBrain

CACHE_DIR = Path("data/ai_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = CACHE_DIR / "market_scan.json"

def save_market_scan(limit=200):
    brain = MarketBrain()
    stocks = brain.scan(limit=limit)

    data = []
    for s in stocks:
        data.append({
            "symbol": s.symbol,
            "name": s.name,
            "price": s.price,
            "ai_score": s.ai_score,
            "technical_score": s.technical_score,
            "fundamental_score": s.fundamental_score,
            "chip_score": s.chip_score,
            "news_score": s.news_score,
            "support": s.support,
            "resistance": s.resistance,
            "target_price": s.target_price,
            "stop_loss": s.stop_loss,
            "breakout_probability": s.breakout_probability,
            "recommendation": s.recommendation,
            "reasons": s.reasons,
        })

    data = sorted(data, key=lambda x: x["ai_score"], reverse=True)

    payload = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "count": len(data),
        "stocks": data
    }

    CACHE_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"✅ AI Market Cache 已建立：{CACHE_FILE}")
    print(f"✅ 股票數量：{len(data)}")

def load_market_scan():
    if not CACHE_FILE.exists():
        return None
    return json.loads(CACHE_FILE.read_text(encoding="utf-8"))

if __name__ == "__main__":
    save_market_scan(limit=200)
''', encoding="utf-8")

Path("elsa_build004.py").write_text('''
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

msg = "\\n".join(lines)

print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ Build 004 安裝完成")
