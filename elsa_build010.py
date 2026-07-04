
import json
from pathlib import Path

from manager.real_manager import RealManager
from services.line_service import send_line_message

CACHE = Path("data/ai_cache/market_scan.json")
data = json.loads(CACHE.read_text(encoding="utf-8"))
stocks = data["stocks"]

manager = RealManager()

lines = []
lines.append("🧑‍💼 Elsa AI Build010")
lines.append("真正的股票經理人決策")
lines.append("=" * 30)
lines.append(f"資料時間：{data['updated_at']}")
lines.append("")

for stock in stocks[:5]:
    d = manager.analyze(stock)

    lines.append(f"📈 {d['name']}（{d['symbol']}）")
    lines.append(f"AI分數：{d['score']}｜信心：{d['confidence']}%｜風格：{d['tone']}")
    lines.append(f"現價：{d['price']}｜支撐：{d['support']}｜壓力：{d['resistance']}")
    lines.append(f"停損：{d['stop_loss']}｜目標：{d['target']}")
    lines.append(f"風險：{d['risk_pct']}%｜預期報酬：{d['reward_pct']}%｜風報比：1:{d['rr']}")
    lines.append(f"買點1：{d['buy_zone_1']}｜買點2：{d['buy_zone_2']}｜突破加碼：{d['add_zone']}")
    lines.append(f"停利1：{d['take_profit_1']}｜停利2：{d['take_profit_2']}")
    lines.append("經理人說：")
    for t in d["manager_text"]:
        lines.append(f"・{t}")
    lines.append("理由：")
    for r in d["reasons"][:3]:
        lines.append(f"✔ {r}")
    lines.append("-" * 30)

lines.append("📌 今日總結")
lines.append("高分不等於立刻買。Elsa 會同時看 AI 分數、突破率、壓力距離與風險報酬比。")

msg = "\n".join(lines)

Path("reports/build010_real_manager_report.txt").write_text(msg, encoding="utf-8")

print(msg)
send_line_message(msg)
