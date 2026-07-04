from pathlib import Path

Path("manager/real_manager.py").write_text('''
class RealManager:

    def analyze(self, stock):
        price = stock["price"]
        support = stock["support"]
        resistance = stock["resistance"]
        stop_loss = stock["stop_loss"]
        target = stock["target_price"]
        score = stock["ai_score"]
        breakout = stock["breakout_probability"]

        risk_pct = 0
        reward_pct = 0
        rr = 0

        if price and stop_loss and price > stop_loss:
            risk_pct = round((price - stop_loss) / price * 100, 2)

        if price and target and target > price:
            reward_pct = round((target - price) / price * 100, 2)

        if risk_pct > 0:
            rr = round(reward_pct / risk_pct, 2)

        confidence = min(95, max(30, int(
            score * 0.55 +
            breakout * 0.25 +
            stock["technical_score"] * 0.10 +
            stock["chip_score"] * 0.10
        )))

        if score >= 80 and breakout >= 75 and rr >= 2:
            action = "可列入重點進場觀察，等待帶量突破後分批布局"
            tone = "偏積極"
        elif score >= 70 and rr >= 1.5:
            action = "續抱觀察，不建議追高，等待更好買點"
            tone = "穩健"
        elif score >= 60:
            action = "中性觀察，暫時不要急著進場"
            tone = "保守"
        else:
            action = "暫不進場，先避開風險"
            tone = "防守"

        buy_zone_1 = round(support * 1.01, 2) if support else 0
        buy_zone_2 = round(support * 0.99, 2) if support else 0
        add_zone = round(resistance * 1.01, 2) if resistance else 0
        take_profit_1 = target
        take_profit_2 = round(target * 1.04, 2) if target else 0

        manager_text = []

        manager_text.append(f"今天操作風格：{tone}")
        manager_text.append(action)

        if resistance and price:
            distance_to_resistance = round((resistance - price) / price * 100, 2)
            if distance_to_resistance <= 1:
                manager_text.append("目前距離壓力區很近，不適合盲目追高。")
            elif distance_to_resistance <= 3:
                manager_text.append("股價接近壓力區，適合等突破確認。")

        if rr < 1:
            manager_text.append("目前風險報酬比不漂亮，建議等待更好的價格。")
        elif rr >= 2:
            manager_text.append("風險報酬比尚可，若量能配合可以列入觀察。")

        return {
            "name": stock["name"],
            "symbol": stock["symbol"],
            "score": score,
            "confidence": confidence,
            "tone": tone,
            "action": action,
            "price": price,
            "support": support,
            "resistance": resistance,
            "stop_loss": stop_loss,
            "target": target,
            "risk_pct": risk_pct,
            "reward_pct": reward_pct,
            "rr": rr,
            "buy_zone_1": buy_zone_1,
            "buy_zone_2": buy_zone_2,
            "add_zone": add_zone,
            "take_profit_1": take_profit_1,
            "take_profit_2": take_profit_2,
            "manager_text": manager_text,
            "reasons": stock.get("reasons", [])[:5],
        }
''', encoding="utf-8")

Path("elsa_build010.py").write_text('''
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

msg = "\\n".join(lines)

Path("reports/build010_real_manager_report.txt").write_text(msg, encoding="utf-8")

print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ Build010 安裝完成")
