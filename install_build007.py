from pathlib import Path

Path("manager").mkdir(exist_ok=True)

Path("manager/decision_manager.py").write_text('''
class DecisionManager:

    def decide(self, stock):
        score = stock["ai_score"]
        breakout = stock["breakout_probability"]
        price = stock["price"]
        resistance = stock["resistance"]
        support = stock["support"]

        if score >= 80 and breakout >= 75:
            action = "可列入今日重點觀察，等待帶量突破再分批布局"
            level = "★★★★★"
        elif score >= 70:
            action = "續抱 / 觀察，不追高"
            level = "★★★★"
        elif score >= 60:
            action = "中性觀察，等待更明確訊號"
            level = "★★★"
        else:
            action = "暫不進場，風險偏高"
            level = "★★"

        reasons = []

        if resistance and price:
            distance = round((resistance - price) / price * 100, 2)
            if distance <= 1:
                reasons.append("距離壓力區很近，不適合盲目追高")
            elif distance <= 3:
                reasons.append("接近壓力區，需觀察是否帶量突破")

        if support and price:
            down_risk = round((price - support) / price * 100, 2)
            reasons.append(f"距離支撐約 {down_risk}%")

        for r in stock.get("reasons", [])[:3]:
            reasons.append(r)

        return {
            "name": stock["name"],
            "symbol": stock["symbol"],
            "score": score,
            "level": level,
            "action": action,
            "price": price,
            "support": support,
            "resistance": resistance,
            "breakout": breakout,
            "reasons": reasons[:6]
        }
''', encoding="utf-8")

Path("elsa_build007.py").write_text('''
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

msg = "\\n".join(lines)

Path("reports/build007_manager_report.txt").write_text(msg, encoding="utf-8")

print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ Build 007 安裝完成")
