
import json
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from scanner.market_cache import save_market_scan, load_market_scan
from portfolio.portfolio_center import PortfolioCenter
from portfolio.portfolio_health import PortfolioHealth

BRAIN_FILE = Path("data/ai_cache/elsa_brain.json")
BRAIN_FILE.parent.mkdir(parents=True, exist_ok=True)

class ElsaBrain:

    def update(self, limit=200):
        save_market_scan(limit=limit)

        market = load_market_scan()
        portfolio = PortfolioCenter().analyze()
        health = PortfolioHealth().calculate(portfolio)

        stocks = market["stocks"]

        top10 = stocks[:10]
        elite = [s for s in stocks if s["ai_score"] >= 75][:3]
        watch = [s for s in stocks if 60 <= s["ai_score"] < 75][:10]
        avoid = [s for s in stocks if s["ai_score"] < 55][:10]

        market_score = round(sum(s["ai_score"] for s in top10) / len(top10)) if top10 else 0

        brain = {
            "updated_at": datetime.now(ZoneInfo("Asia/Taipei")).strftime("%Y-%m-%d %H:%M:%S"),
            "market": {
                "score": market_score,
                "count": market["count"],
                "top10": top10,
                "elite": elite,
                "watch": watch,
                "avoid": avoid
            },
            "portfolio": portfolio,
            "portfolio_health": health
        }

        BRAIN_FILE.write_text(
            json.dumps(brain, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        return brain

    def load(self):
        if not BRAIN_FILE.exists():
            return None
        return json.loads(BRAIN_FILE.read_text(encoding="utf-8"))
