
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
