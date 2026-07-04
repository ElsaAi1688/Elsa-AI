from pathlib import Path

Path("core").mkdir(exist_ok=True)

Path("core/elsa_brain.py").write_text('''
import json
from pathlib import Path
from datetime import datetime

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
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
''', encoding="utf-8")

Path("elsa_core.py").write_text('''
from core.elsa_brain import ElsaBrain
from services.line_service import send_line_message

brain = ElsaBrain().update(limit=200)

lines = []
lines.append("🧠 Elsa Core Brain 已更新")
lines.append("=" * 30)
lines.append(f"更新時間：{brain['updated_at']}")
lines.append(f"市場分數：{brain['market']['score']}/100")
lines.append(f"掃描股票數：{brain['market']['count']}")
lines.append(f"投資健康度：{brain['portfolio_health']['score']}/100｜{brain['portfolio_health']['level']}")
lines.append("")
lines.append("🔥 今日 Top3")
for i, s in enumerate(brain["market"]["top10"][:3], 1):
    lines.append(f"{i}. {s['name']} AI {s['ai_score']}")

msg = "\\n".join(lines)
print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ Sprint 4-A Elsa Core Brain 安裝完成")
