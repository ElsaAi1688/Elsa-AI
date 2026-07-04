from pathlib import Path

Path("alerts").mkdir(exist_ok=True)

Path("alerts/alert_engine.py").write_text('''
class AlertEngine:

    def generate_alerts(self, stocks):
        alerts = []

        for s in stocks:
            name = s["name"]
            score = s["ai_score"]
            breakout = s["breakout_probability"]
            price = s["price"]
            resistance = s["resistance"]
            stop_loss = s["stop_loss"]

            if score >= 85:
                alerts.append(f"🚨 {name} 進入強勢名單｜AI {score}")

            if breakout >= 80:
                alerts.append(f"🚀 {name} 突破機率 {breakout}%｜可列入盤中觀察")

            if price and resistance and price >= resistance * 0.99:
                alerts.append(f"⚡ {name} 接近壓力 {resistance}｜等待帶量突破")

            if price and stop_loss and price <= stop_loss:
                alerts.append(f"⚠️ {name} 跌破停損 {stop_loss}｜注意風險")

        return alerts[:10]
''', encoding="utf-8")

Path("elsa_build009.py").write_text('''
import json
from pathlib import Path

from alerts.alert_engine import AlertEngine
from services.line_service import send_line_message

CACHE = Path("data/ai_cache/market_scan.json")
data = json.loads(CACHE.read_text(encoding="utf-8"))
stocks = data["stocks"]

alerts = AlertEngine().generate_alerts(stocks)

lines = []
lines.append("🚨 Elsa AI Build 009")
lines.append("盤中 Alert 事件通知")
lines.append("=" * 30)

if alerts:
    lines.extend(alerts)
else:
    lines.append("目前沒有觸發重大事件。")

lines.append("")
lines.append("Alert 條件：AI高分、突破率高、接近壓力、跌破停損。")

msg = "\\n".join(lines)

Path("reports/build009_alert_report.txt").write_text(msg, encoding="utf-8")

print(msg)
send_line_message(msg)
''', encoding="utf-8")

print("✅ Build 009 安裝完成")
